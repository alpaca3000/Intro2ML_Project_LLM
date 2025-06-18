from huggingface_hub import create_repo, upload_folder

repo_name = "en-vi-translation-model"
create_repo(repo_name, private=False)  # hoặc private=True nếu muốn riêng tư

upload_folder(
    repo_id="alpaca3000/en-vi-translation-model",  # Thay bằng username của bạn
    folder_path="models/my_en_vi_translation_model_archive",
    path_in_repo="",  # để giữ nguyên cấu trúc thư mục
    commit_message="Initial model upload"
)
