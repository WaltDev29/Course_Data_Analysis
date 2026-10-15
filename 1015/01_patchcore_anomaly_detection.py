"""
PatchCore 기반 이상 탐지 실습 코드
Anomaly Detection

개요
    정상 이미지만으로 메모리 뱅크를 구축하고, 테스트 이미지의 패치와
    메모리 뱅크 사이의 최근접 이웃 거리를 이상 점수로 사용한다.
    역전파 학습이 없으므로 1회 순회로 학습이 완료된다.

사전 준비
    pip install "anomalib[cpu]"        # CPU 환경
    pip install "anomalib[cu130]"      # CUDA 환경 (버전은 설치 환경에 맞춘다)
    pip install matplotlib

실행 예시
    python patchcore_anomaly_detection.py train   --category bottle
    python patchcore_anomaly_detection.py custom  --root ./dataset/my_parts
    python patchcore_anomaly_detection.py predict --ckpt results/.../model.ckpt --images ./test_images
    python patchcore_anomaly_detection.py score   --ckpt results/.../model.ckpt
    python patchcore_anomaly_detection.py export  --ckpt results/.../model.ckpt
"""

import argparse
import sys
from pathlib import Path

# anomalib은 데이터 경로에 한글 등 ASCII 외 문자가 있으면 오류를 내므로 데이터는 영문 경로에 둔다
WORK_DIR = Path(__file__).resolve().parents[1]

import numpy as np

from anomalib.data import Folder, MVTecAD, PredictDataset
from anomalib.deploy import ExportType
from anomalib.engine import Engine
from anomalib.models import Patchcore


# ----------------------------------------------------------------------
# 공통 : 모델 생성
# ----------------------------------------------------------------------
def build_model(coreset_ratio: float = 0.1, num_neighbors: int = 9) -> Patchcore:
    """PatchCore 모델을 생성한다.

    backbone
        ImageNet 사전학습 WideResNet-50 을 사용한다.
    layers
        layer2 와 layer3 의 중간 특징을 사용한다. 최종층은 ImageNet 분류에
        치우쳐 있어 제외한다.
    coreset_sampling_ratio
        메모리 뱅크에 남길 패치의 비율이다. 값을 낮추면 추론이 빨라지고
        메모리 사용량이 줄어드는 대신 정확도가 하락할 수 있다.
    num_neighbors
        이상 점수를 산정할 때 참조하는 최근접 이웃의 개수이다.
    """
    return Patchcore(
        backbone="wide_resnet50_2",
        layers=["layer2", "layer3"],
        coreset_sampling_ratio=coreset_ratio,
        num_neighbors=num_neighbors,
    )


# ----------------------------------------------------------------------
# 1. MVTec AD 학습 및 평가
# ----------------------------------------------------------------------
def run_train(args) -> None:
    """MVTec AD 의 한 카테고리로 학습하고 평가 지표를 출력한다.

    데이터가 없으면 anomalib 이 자동으로 내려받는다.
    학습 세트에는 정상 이미지만 포함되어 있어야 한다.
    """
    datamodule = MVTecAD(
        root=args.data_root,
        category=args.category,
        train_batch_size=args.batch_size,
        eval_batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    model = build_model(args.coreset_ratio, args.num_neighbors)

    # PatchCore 는 역전파 학습이 없으므로 max_epochs 는 1 로 고정한다.
    engine = Engine(max_epochs=1)

    engine.fit(model=model, datamodule=datamodule)
    results = engine.test(model=model, datamodule=datamodule)

    print("\n[평가 결과]")
    for row in results:
        for key, value in row.items():
            print(f"  {key:<28} {value:.4f}" if isinstance(value, float) else f"  {key:<28} {value}")
    print("\n체크포인트와 결과 이미지는 results/ 폴더 아래에 저장된다.")


# ----------------------------------------------------------------------
# 2. 자체 촬영 데이터 학습
# ----------------------------------------------------------------------
def run_custom(args) -> None:
    """직접 수집한 이미지로 학습한다.

    요구되는 폴더 구조
        <root>/
        ├─ good/       정상 이미지 (학습에 사용)
        ├─ defect/     결함 이미지 (평가에만 사용, 선택)
        └─ mask/       결함 마스크 (선택, 화소 단위 평가 시 필요)

    good 폴더에 결함 이미지가 섞이면 정상 분포가 오염되어 검출률이 떨어진다.
    촬영 시 조명과 카메라 거리를 고정해야 성능이 안정된다.
    """
    root = Path(args.root)
    if not (root / args.normal_dir).exists():
        raise FileNotFoundError(f"정상 이미지 폴더가 없다: {root / args.normal_dir}")

    datamodule = Folder(
        name=root.name,
        root=root,
        normal_dir=args.normal_dir,
        abnormal_dir=args.abnormal_dir,
        mask_dir=args.mask_dir,
        train_batch_size=args.batch_size,
        eval_batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    model = build_model(args.coreset_ratio, args.num_neighbors)
    engine = Engine(max_epochs=1)

    engine.fit(model=model, datamodule=datamodule)

    # 결함 이미지가 준비된 경우에만 평가가 의미를 가진다.
    if args.abnormal_dir and (root / args.abnormal_dir).exists():
        engine.test(model=model, datamodule=datamodule)
    else:
        print("결함 이미지 폴더가 없어 평가 단계를 건너뛴다.")


# ----------------------------------------------------------------------
# 3. 추론 및 히트맵 저장
# ----------------------------------------------------------------------
def run_predict(args) -> None:
    """학습된 체크포인트로 폴더 안의 이미지를 판정한다.

    출력
        이미지별 이상 점수와 판정 결과를 표준 출력에 표시하고,
        이상 맵을 원본 위에 겹친 이미지를 out 폴더에 저장한다.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    dataset = PredictDataset(path=args.images, image_size=(256, 256))
    model = build_model(args.coreset_ratio, args.num_neighbors)
    engine = Engine()

    predictions = engine.predict(model=model, dataset=dataset, ckpt_path=args.ckpt)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'파일명':<32}{'이상 점수':>12}  판정")
    print("-" * 58)

    for batch in predictions:
        # 결과는 배치 단위로 반환되므로 요소 단위로 풀어서 처리한다.
        paths = _as_list(batch.image_path)
        scores = _as_list(batch.pred_score)
        labels = _as_list(batch.pred_label)
        maps = batch.anomaly_map

        for i, path in enumerate(paths):
            score = float(np.asarray(scores[i]).item())
            label = int(np.asarray(labels[i]).item())
            verdict = "이상" if label == 1 else "정상"
            print(f"{Path(path).name:<32}{score:>12.4f}  {verdict}")

            if maps is None:
                continue

            anomaly_map = np.asarray(maps[i]).squeeze()
            image = plt.imread(path)

            fig, axes = plt.subplots(1, 3, figsize=(12, 4))
            axes[0].imshow(image)
            axes[0].set_title("input")
            axes[1].imshow(anomaly_map, cmap="jet")
            axes[1].set_title("anomaly map")
            axes[2].imshow(image)
            axes[2].imshow(
                _resize_map(anomaly_map, image.shape[:2]), cmap="jet", alpha=0.45
            )
            axes[2].set_title(f"{verdict}  score={score:.3f}")
            for ax in axes:
                ax.axis("off")
            fig.tight_layout()
            fig.savefig(out_dir / f"{Path(path).stem}_result.png", dpi=120)
            plt.close(fig)

    print(f"\n결과 이미지는 {out_dir} 폴더에 저장되었다.")


# ----------------------------------------------------------------------
# 4. 이상 점수 분포와 임계값 시각화
# ----------------------------------------------------------------------
# 테스트 폴더 이름을 그래프에 표시할 한글 이름으로 바꾼다(없으면 폴더 이름 그대로)
DEFECT_NAMES = {"good": "정상", "broken_large": "큰 파손", "broken_small": "작은 파손", "contamination": "오염"}


def run_score(args) -> None:
    """정상 기준 표준화 점수로 테스트 이미지를 점찍어 임계값과 함께 그린다.

    점수 정의
        이상 맵의 각 화소를 (값 - 정상 평균) / 정상 표준편차 로 표준화하고
        이미지 안의 최댓값을 이상 점수로 쓴다. 정상 평균과 표준편차는
        학습용 정상 이미지(train/good)의 이상 맵에서 구한다.
    임계값
        점수가 임계값 이상이면 결함으로 본다. 낮추면 놓침이 줄고 오판이 늘며,
        높이면 오판이 줄고 놓침이 는다.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import torch
    from PIL import Image
    from torchvision.transforms.v2.functional import to_dtype, to_image

    plt.rcParams["font.family"] = "Malgun Gothic"  # 한글 폰트 설정
    plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지

    model = Patchcore.load_from_checkpoint(args.ckpt, map_location="cpu").eval()

    def anomaly_maps(folder: Path) -> np.ndarray:
        """폴더 안 이미지의 원래(정규화 전) 이상 맵을 모은다."""
        maps = []
        for path in sorted(folder.glob("*.png")):
            image = to_dtype(to_image(Image.open(path).convert("RGB")), torch.float32, scale=True)
            with torch.no_grad():
                output = model.model(model.pre_processor(image[None]))
            maps.append(output.anomaly_map.squeeze().numpy())
        return np.stack(maps)

    root = Path(args.data_root) / args.category

    # 정상 기준 : 학습용 정상 이미지 이상 맵의 평균과 표준편차
    normal = anomaly_maps(root / "train" / "good")
    mean, std = normal.mean(), normal.std()

    # 테스트 폴더별 이상 점수(정상 good 을 맨 앞에 둔다)
    folders = sorted((root / "test").iterdir(), key=lambda p: (p.name != "good", p.name))
    scores = {}
    for folder in folders:
        z = (anomaly_maps(folder) - mean) / std
        scores[folder.name] = z.reshape(len(z), -1).max(axis=1)

    # 점 그래프 : 정상은 맨 위, 결함 종류는 한 칸 띄우고 아래로
    fig, ax = plt.subplots(figsize=(11, 5.5))
    y_pos, y = {}, 0
    for name in scores:
        y_pos[name] = y
        y -= 2 if name == "good" else 1
    for name, z in scores.items():
        color = "#2e9b5e" if name == "good" else "#d94848"
        ax.scatter(z, [y_pos[name]] * len(z), s=120, color=color, alpha=0.8, edgecolors="none")

    defect_count = sum(len(z) for name, z in scores.items() if name != "good")
    defect_kinds = "·".join(DEFECT_NAMES.get(n, n) for n in scores if n != "good")
    ax.scatter([], [], s=120, color="#2e9b5e", label=f"정상 테스트 {len(scores.get('good', []))}장")
    ax.scatter([], [], s=120, color="#d94848", label=f"결함 테스트 {defect_count}장 ({defect_kinds})")
    ax.legend(loc="upper right", frameon=False, fontsize=11)

    # 임계값 선과 설명
    ax.axvline(args.threshold, color="#3a5fcd", linestyle="--", linewidth=2.5)
    top = max(y_pos.values()) + 1.2
    bottom = min(y_pos.values()) - 1.0
    ax.text(args.threshold + 0.1, top - 0.3, f"임계값 {args.threshold:.1f}",
            color="#3a5fcd", fontsize=15, fontweight="bold", va="top")
    ax.text(args.threshold - 0.1, bottom + 0.1, "◀ 낮추면 : 놓침 감소, 오판 증가",
            ha="right", va="bottom", fontsize=11, color="#555555")
    ax.text(args.threshold + 0.1, bottom + 0.1, "높이면 : 오판 감소, 놓침 증가 ▶",
            ha="left", va="bottom", fontsize=11, color="#555555")

    # 축 정리
    ax.set_yticks(list(y_pos.values()))
    ax.set_yticklabels([DEFECT_NAMES.get(n, n) for n in y_pos], fontsize=12)
    ax.set_ylim(bottom - 0.6, top)
    all_scores = np.concatenate(list(scores.values()))
    ax.set_xlim(min(1, all_scores.min() - 0.5), all_scores.max() + 0.7)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))  # x축 눈금 1 간격
    ax.set_xlabel("이상 점수 (정상 평균에서 벗어난 정도 ÷ 정상 편차, 이미지 내 최대값)", fontsize=12)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(args.out, dpi=120)
    plt.close(fig)

    # 임계값 기준 판정 결과
    print(f"\n임계값 {args.threshold:.1f} 기준 판정")
    for name, z in scores.items():
        wrong = (z >= args.threshold) if name == "good" else (z < args.threshold)
        kind = "오판(정상을 결함으로)" if name == "good" else "놓침(결함을 정상으로)"
        print(f"  {DEFECT_NAMES.get(name, name):<8} {len(z):>3}장  점수 {z.min():5.2f} ~ {z.max():5.2f}  {kind} {int(wrong.sum())}장")
    print(f"\n그래프는 {args.out} 에 저장되었다.")


# ----------------------------------------------------------------------
# 5. OpenVINO 내보내기
# ----------------------------------------------------------------------
def run_export(args) -> None:
    """엣지 배포용으로 모델을 내보낸다.

    OpenVINO 형식으로 변환하면 CPU 환경에서의 추론 속도가 개선된다.
    변환 전후의 FPS 를 비교해 보는 것을 권장한다.
    """
    model = build_model(args.coreset_ratio, args.num_neighbors)
    engine = Engine()
    engine.export(
        model=model,
        export_type=ExportType.OPENVINO,
        ckpt_path=args.ckpt,
    )
    print("내보내기가 완료되었다. results/ 폴더 아래의 weights 경로를 확인한다.")


# ----------------------------------------------------------------------
# 보조 함수
# ----------------------------------------------------------------------
def _as_list(value):
    """스칼라와 배치 출력을 동일한 형태로 취급한다."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    arr = np.asarray(value)
    return arr.tolist() if arr.ndim > 0 else [arr]


def _resize_map(anomaly_map: np.ndarray, shape) -> np.ndarray:
    """이상 맵을 원본 이미지 크기로 확대한다."""
    try:
        import cv2

        return cv2.resize(anomaly_map, (shape[1], shape[0]))
    except ImportError:
        ys = (np.linspace(0, anomaly_map.shape[0] - 1, shape[0])).astype(int)
        xs = (np.linspace(0, anomaly_map.shape[1] - 1, shape[1])).astype(int)
        return anomaly_map[np.ix_(ys, xs)]


# ----------------------------------------------------------------------
# 진입점
# ----------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PatchCore 기반 이상 탐지 실습",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # 공통 인자
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--coreset-ratio", type=float, default=0.1, help="메모리 뱅크 축소 비율")
    common.add_argument("--num-neighbors", type=int, default=9, help="점수 산정에 사용할 이웃 수")
    common.add_argument("--batch-size", type=int, default=8, help="배치 크기")
    common.add_argument("--num-workers", type=int, default=4, help="데이터 로더 워커 수")

    p_train = sub.add_parser("train", parents=[common], help="MVTec AD 학습 및 평가")
    p_train.add_argument("--category", default="bottle", help="MVTec AD 카테고리 이름")
    p_train.add_argument("--data-root", default=str(WORK_DIR / "data"), help="데이터셋 경로")
    p_train.set_defaults(func=run_train)

    p_custom = sub.add_parser("custom", parents=[common], help="자체 촬영 데이터 학습")
    p_custom.add_argument("--root", required=True, help="데이터 최상위 폴더")
    p_custom.add_argument("--normal-dir", default="good", help="정상 이미지 폴더 이름")
    p_custom.add_argument("--abnormal-dir", default="defect", help="결함 이미지 폴더 이름")
    p_custom.add_argument("--mask-dir", default=None, help="결함 마스크 폴더 이름")
    p_custom.set_defaults(func=run_custom)

    p_pred = sub.add_parser("predict", parents=[common], help="이미지 폴더 추론")
    p_pred.add_argument("--ckpt", required=True, help="학습된 체크포인트 경로")
    p_pred.add_argument("--images", required=True, help="추론할 이미지 폴더")
    p_pred.add_argument("--out", default="./predict_out", help="결과 이미지 저장 폴더")
    p_pred.set_defaults(func=run_predict)

    p_score = sub.add_parser("score", parents=[common], help="이상 점수 분포와 임계값 그래프")
    p_score.add_argument("--ckpt", required=True, help="학습된 체크포인트 경로")
    p_score.add_argument("--category", default="bottle", help="MVTec AD 카테고리 이름")
    p_score.add_argument("--data-root", default=str(WORK_DIR / "data"), help="데이터셋 경로")
    p_score.add_argument("--threshold", type=float, default=3.0, help="결함 판정 임계값")
    p_score.add_argument("--out", default="./score_plot.png", help="그래프 저장 파일")
    p_score.set_defaults(func=run_score)

    p_exp = sub.add_parser("export", parents=[common], help="OpenVINO 내보내기")
    p_exp.add_argument("--ckpt", required=True, help="학습된 체크포인트 경로")
    p_exp.set_defaults(func=run_export)

    return parser


if __name__ == "__main__":
    # VS Code에서 인자 없이 실행하면 train 모드로 실행한다
    argv = sys.argv[1:] or ["train"]
    args = build_parser().parse_args(argv)
    args.func(args)
