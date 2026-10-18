export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartPaddingPanel.test.tsx"], maxWorkers: 1, fileParallelism: false },
};
