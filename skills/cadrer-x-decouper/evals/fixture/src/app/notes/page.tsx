import { listNotes } from "@/modules/notes/server";
import { Card } from "@/components/Card";

export default async function NotesPage() {
  const notes = await listNotes();
  if (notes.length === 0) return <main><p>Tu n'as pas encore de note. Ajoute ta première note depuis un livre.</p></main>;
  return (
    <main>
      <h1>Tes notes</h1>
      {notes.map((n) => <Card key={n.id} title={n.book} meta={n.page ? `p. ${n.page}` : undefined} href={`/notes/${n.id}`}>{n.text}</Card>)}
    </main>
  );
}
