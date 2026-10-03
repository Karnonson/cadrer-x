import { currentMember } from "@/modules/accounts/server";
import { notesOf, noteOf } from "../data/notes";

export async function listNotes() {
  const member = await currentMember();
  return notesOf(member.id);
}

export async function getNote(id: string) {
  const member = await currentMember();
  return noteOf(member.id, id);
}
