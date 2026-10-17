export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartSetupPanel.test.tsx"], maxWorkers: 1, fileParallelism: false },
};


