import { describe, expect, it } from "vitest";
import { formatBytes, scoreTone, validateResumeFile, wordCount } from "./format";

describe("formatBytes", () => {
  it("formats kilobytes and megabytes", () => {
    expect(formatBytes(2048)).toBe("2.0 KB");
    expect(formatBytes(2 * 1024 * 1024)).toBe("2.0 MB");
  });
});

describe("wordCount", () => {
  it("counts words and ignores extra spaces", () => {
    expect(wordCount("  hello   world  ")).toBe(2);
    expect(wordCount("")).toBe(0);
  });
});

describe("scoreTone", () => {
  it("uses documented thresholds", () => {
    expect(scoreTone(81)).toBe("excellent");
    expect(scoreTone(70)).toBe("strong");
    expect(scoreTone(50)).toBe("moderate");
    expect(scoreTone(10)).toBe("needs");
  });
});

describe("validateResumeFile", () => {
  it("rejects unsupported types and oversized files", () => {
    const png = new File(["x"], "photo.png", { type: "image/png" });
    expect(validateResumeFile(png)).toMatch(/Unsupported file type/);

    const huge = new File([new Uint8Array(6 * 1024 * 1024)], "resume.pdf", { type: "application/pdf" });
    expect(validateResumeFile(huge)).toMatch(/too large/);
  });

  it("accepts a small text resume", () => {
    const file = new File(["jordan hale software engineer"], "resume.txt", { type: "text/plain" });
    expect(validateResumeFile(file)).toBeNull();
  });
});
