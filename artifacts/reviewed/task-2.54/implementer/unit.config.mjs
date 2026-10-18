export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartBackgroundPanel.test.tsx"], maxWorkers: 1, fileParallelism: false },
};
