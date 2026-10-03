export async function currentMember(): Promise<{ id: string; displayName: string }> {
  // Better Auth's session in the real app; the tests stub this module.
  throw new Error("no session");
}
