from pathlib import Path

def save_graph_as_png(app, path="agent_graph.png"):
    """Lưu đồ thị ra file ảnh."""
    if Path("agent_graph.png").exists():
        return

    try:
        image_data = app.get_graph().draw_mermaid_png()
        with open(path, "wb") as f:
            f.write(image_data)
        print(f"✅ Đã lưu đồ thị tại: {path}")
    except Exception as e:
        print(f"❌ Không thể tạo ảnh: {e}")
        print("💡 Gợi ý: In mã Mermaid ra để xem online:")
        print(app.get_graph().draw_mermaid())

