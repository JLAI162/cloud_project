## CGU雲端系統課程 mini project 
LLM with search <br>
v1. 此系統使用 Ollama 軟體跑本地端的大型語言模型搭配 wiki 查詢爬蟲作為服務，呈現於瀏覽器前端網頁。運用 docker 部屬 container 形成多節點系統，並由 nginx 的 load balencer 功能協調任務分配。<br>
v2. 此系統改使用 ScrapeGraphAI 加強網路搜尋功能，取代原侷限於wiki的搜尋功能，且使用 slurm 軟體作為任務分配器，運用 slurm 已實現的各式管理功能。另外v2將服務以 line bot 的方式供使用者互動 <br>
