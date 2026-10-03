import { db } from "@/modules/shared-db";

export type NoteRow = { id: string; book: string; page: number | null; text: string; created_at: string };

export async function notesOf(memberId: string): Promise<NoteRow[]> {
  const r = await db.execute({
    sql: "select n.id, b.title as book, n.page, n.text, n.created_at from notes n join books b on b.id = n.book_id where n.member_id = ? order by n.created_at desc",
    args: [memberId],
  });
  return r.rows as unknown as NoteRow[];
}

export async function noteOf(memberId: string, id: string): Promise<NoteRow | null> {
  const r = await db.execute({
    sql: "select n.id, b.title as book, n.page, n.text, n.created_at from notes n join books b on b.id = n.book_id where n.member_id = ? and n.id = ?",
    args: [memberId, id],
  });
  return (r.rows[0] as unknown as NoteRow) ?? null;
}
