# QOpenBB

QOpenBB is a self-hosted OpenBB workspace for financial research. Use it to compare a company's reported and estimated earnings, inspect filings and transcripts, or put company financials alongside FRED economic series. Docker Compose runs the browser workspace and the data API together. The data API uses your FMP and FRED keys to retrieve observations.

## Start with Docker Compose

You need a Linux or WSL x86-64 host, Docker with the Compose plugin, and API keys for Financial Modeling Prep (FMP) and FRED. The two images are public. The commands below install the published development alpha in a new directory. [Release and verification](verification/earnings-calendar/README.md#published-alpha)

1. Download the Compose file and environment template from the same release.

   ```bash
   mkdir qopenbb && cd qopenbb
   release=https://github.com/norandom/QOpenBB/releases/download/alpha-46047645104-1
   curl -fsSLo compose.yaml "$release/compose.yaml"
   umask 077
   curl -fsSLo .env "$release/default.env.sample"
   mkdir -p data/workspace
   ```

2. Edit `.env`. Enter your `FMP_API_KEY` and `FRED_API_KEY`. For a local install, set `WORKSPACE_BIND_IP=127.0.0.1` and keep `PUBLIC_URL=http://127.0.0.1:23003`. Set both image references below to run the build verified for this guide. For a shared server, configure the browser-facing origin and access controls before starting. [Remote access](docs/tips-and-tricks.md)

   ```dotenv
   WORKSPACE_IMAGE=ghcr.io/norandom/qopenbb-workspace:alpha-46047645104-1
   DATA_API_IMAGE=ghcr.io/norandom/qopenbb-data-api:alpha-46047645104-1
   ```

3. Start the services and check that `data-api` reports `healthy` and `workspace` is running.

   ```bash
   docker compose config --quiet
   docker compose pull
   docker compose up -d --no-build
   docker compose ps
   ```

## Open your first dashboard

Open <http://127.0.0.1:23003>. If you left the administrator settings blank, run `docker compose exec workspace credentials` in a private terminal to get your login.

1. Open **Connections → Connect Backend**. Give the connection a name and enter `http://127.0.0.1:23003/data`. For a remote install, append `/data` to the origin you opened in your browser.
2. Select **Test**, then **add**. Each Workspace account makes this connection once.
3. Open **Apps → QOpenBB starter**. Check that the AAPL annual income widget shows a fiscal period and a value, and that the FRED GDP widget shows a dated observation. These checks exercise both provider connections. If a widget stays empty, check the connection URL, provider keys and dataset access. [Installation and troubleshooting](docs/install.md#check-startup-problems)

Keep `.env` and `data/workspace/` in the same deployment directory across updates. The latter holds account connections and saved dashboards. [Persistence and updates](docs/install.md#persistence-and-updates)

[Documentation by concern](docs/index.md) · [Company research](docs/company-research.md) · [Chart gallery](docs/chart-gallery.md)
