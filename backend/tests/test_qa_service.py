from app.services.qa_service import QAService


def test_qa_service_passed():
    eval_res = QAService.evaluate(
        headline="Strategi Efektif Follow Up Leads Iklan Properti",
        body_caption="Berikut adalah 3 langkah penting dalam mengelola leads properti dari iklan agar tidak dingin dan mempermudah tim sales.",
        category_badge="MARKETING"
    )
    assert eval_res["status"] == "PASSED"
    assert len(eval_res["issues"]) == 0


def test_qa_service_prohibited_claim():
    eval_res = QAService.evaluate(
        headline="Investasi Rukos Pasti Untung 100% Bebas Risiko",
        body_caption="Beli unit sekarang dan pasti untung 100% setiap bulan.",
        category_badge="INVESTASI"
    )
    assert eval_res["status"] == "FAILED"
    assert any("pasti untung" in issue for issue in eval_res["issues"])
