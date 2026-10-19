# Tips and Tricks

The [development installation](install.md) runs locally using prebuilt alpha images. These options adapt that setup to your environment.

## Use an existing Cloudflare tunnel

QOpenBB serves plain HTTP on host port 23003. When cloudflared runs on the same host, use `http://127.0.0.1:23003` as its origin. When it runs elsewhere, use the reachable host address. `0.0.0.0` is the listening address, not a tunnel destination.

Set `PUBLIC_URL` in `.env` to your public origin, for example `https://qopenbb.example.com`, then recreate the Workspace container:

```bash
docker compose up -d --no-build workspace
```

Manage the tunnel, public HTTPS and Access policies separately. Compose does not install cloudflared or configure origin TLS. Workspace login remains separate from Cloudflare Access.
