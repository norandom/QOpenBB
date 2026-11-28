# QOpenBB

QOpenBB is a self-hosted OpenBB workspace for financial research. Use it to compare a company's reported and estimated earnings, inspect filings and transcripts, or put company financials alongside FRED economic series. Docker Compose runs Workspace, the data API, and the private financial modeling service.

## Start with Docker Compose

Use an x86-64 Linux host with Docker Compose, or Windows with Docker Desktop running **Linux containers**. Have your FMP and FRED API keys ready. Download and extract the [repository ZIP](https://github.com/norandom/QOpenBB/archive/refs/heads/main.zip) or clone the repository. From that directory run the command for your host.

**Linux or WSL with Bash**

```bash
bash setup.sh
```

**Windows PowerShell**

```powershell
powershell -NoProfile -ExecutionPolicy RemoteSigned -File .\setup.ps1
```

The Windows launcher runs `setup.psh`. Setup preserves an existing `.env` and stores generated settings in `.env.setup`. Both installers prompt privately for missing provider keys, pull the images, connect the data backend, and save the bundled dashboards for the initial administrator. At the end, your terminal shows the Workspace URL and initial login. A fresh local installation listens at <http://127.0.0.1:23003>.

## Open your first dashboard

Sign in, complete the profile prompt if shown, and open **My Dashboards**. Choose **QOpenBB starter** for AAPL financials and FRED GDP, **Events and Documents** for earnings and filings, or **Commodities versus Technology** to run a model comparison. **Saved model output** takes a run ID and output ID from a model you have evaluated.

Run setup again from the same directory to pull updates. Workspace and the data API default to `latest`. You can set `WORKSPACE_IMAGE`, `DATA_API_IMAGE`, and `MODELING_IMAGE` to select specific images. [Installation, storage and troubleshooting](docs/install.md)

[Documentation by concern](docs/index.md) · [Company research](docs/company-research.md) · [Chart gallery](docs/chart-gallery.md)
