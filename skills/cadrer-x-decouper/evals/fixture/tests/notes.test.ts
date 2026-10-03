import { describe, expect, it, vi } from "vitest";

vi.mock("@/modules/accounts/server", () => ({ currentMember: async () => ({ id: "m1", displayName: "Marie" }) }));
vi.mock("@/modules/notes/data/notes", () => ({ notesOf: async (id: string) => (id === "m1" ? [{ id: "n1" }] : []), noteOf: async () => null }));

import { listNotes } from "@/modules/notes/server";

describe("notes", () => {
  it("lists the signed-in member's notes only", async () => {
    expect(await listNotes()).toEqual([{ id: "n1" }]);
  });
});
