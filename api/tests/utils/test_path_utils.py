from app.utils.path_utils import assemble_path


def test_assemble_url():
    assert assemble_path(
        "C:\\produce_exchange_hub\\images\\", "profile_picturs", "62c5100b8778dd6aa23a1ced.jpg"
    ) == "C:\\produce_exchange_hub\\images\\profile_picturs\\62c5100b8778dd6aa23a1ced.jpg"
