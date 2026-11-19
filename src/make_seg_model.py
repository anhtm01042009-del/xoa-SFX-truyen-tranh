"""Tao mo hinh nhan dien chi gom nhanh phan doan chu (seg), nhan anh co kich thuoc tuy y.

Mo hinh goc comictextdetector.pt.onnx co dau vao co dinh 1024x1024 va chay ca nhanh
khoanh khung; ban nay bo nhanh khong can de chay nhanh hon va nhan doan anh khong vuong.

Chay (can: pip install onnx):
  python make_seg_model.py ../models/comictextdetector.pt.onnx ../models/ctd_seg.onnx
"""
import sys


def tao_seg(src, dst):
    """Cat nhanh 'seg' tu src, ghi ra dst. Goi duoc ca trong ban dong goi (khong mo tien trinh moi)."""
    import onnx
    from onnx.utils import extract_model

    extract_model(str(src), str(dst), ["images"], ["seg"])
    m = onnx.load(str(dst))
    dims = m.graph.input[0].type.tensor_type.shape.dim
    dims[2].dim_param, dims[3].dim_param = "H", "W"
    for o in m.graph.output:
        for d in o.type.tensor_type.shape.dim[2:]:
            d.ClearField("dim_value")
    onnx.save(m, str(dst))


if __name__ == "__main__":
    tao_seg(sys.argv[1], sys.argv[2])
    print("da tao", sys.argv[2])
