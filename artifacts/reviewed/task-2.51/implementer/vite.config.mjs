import { defineConfig } from "/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/node_modules/vite/dist/node/index.js";
export default defineConfig({
  root: "/mnt/d/Source/QOpenBB/artifacts/task-2.51/implementer", envDir: false,
  resolve: { alias: { react: "/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/react", "react-dom": "/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/react-dom" } },
  server: { host: "127.0.0.1", port: 6021, strictPort: true, fs: { allow: ["/mnt/d/Source/QOpenBB", "/home/mc/qopenbb-work/appearance-deps"] } },
});
