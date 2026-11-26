import type { Page } from "../node_modules/@playwright/test/index.js";
import { expect } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/toolchain";

export async function signIn(page: Page) {
  const origin = process.env.WORKSPACE_FRONTEND_ORIGIN!;
  const password = process.env.JOURNEY_PASSWORD;
  if (!/^http:\/\/127\.0\.0\.1:\d+$/.test(origin) || !password)
    throw new Error("Disposable loopback Workspace login required");
  await page.context().route("**/*", route => {
    const url = new URL(route.request().url());
    return /^https?:$/.test(url.protocol) && url.origin !== origin ? route.abort() : route.continue();
  });
  let entity: Promise<unknown> | undefined;
  page.on("response", response => {
    if (new URL(response.url()).pathname === "/api/pro/user-has-entity") entity = response.finished();
  });
  await page.goto("/login");
  await page.getByLabel("Email", { exact: true }).fill("analyst@example.com");
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Login", exact: true }).click();
  await page.waitForURL(url => /^\/(app|onboarding)(?:\/|$)/.test(url.pathname));
  if (new URL(page.url()).pathname === "/onboarding") {
    await expect.poll(() => Boolean(entity)).toBe(true);
    await entity;
    await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
    await page.getByPlaceholder("Enter your first name").fill("Model");
    await page.getByPlaceholder("Enter your last name").fill("Analyst");
    await page.getByRole("button", { name: "Continue", exact: true }).click();
  }
  await expect(page.locator("#tabs")).toBeVisible();
  const changelog = page.getByRole("dialog").filter({ has: page.getByRole("heading", { name: "Changelog", exact: true }) });
  await page.addLocatorHandler(changelog, () => changelog.getByRole("button", { name: "Close", exact: true }).click());
}

export async function newDashboard(page: Page) {
  await page.locator("#tabs").getByRole("button").first().click();
  await page.getByRole("button", { name: /New Dashboard/ }).click();
  await expect(page).toHaveURL(/\/app\/[\da-f-]{36}$/);
  return new URL(page.url()).pathname;
}

export async function addWidget(page: Page, name: string) {
  const empty = page.getByRole("main").getByRole("button", { name: "Add widgets", exact: true });
  if (await empty.isVisible()) await empty.click();
  else await page.getByTestId("dashboard-toolbar-add-widget-button").click();
  const dialog = page.getByRole("dialog");
  await dialog.getByPlaceholder("Search for widgets", { exact: true }).fill(name);
  await dialog.getByText(name, { exact: true }).click();
  await dialog.getByRole("button", { name: "Add widgets", exact: true }).click();
}
