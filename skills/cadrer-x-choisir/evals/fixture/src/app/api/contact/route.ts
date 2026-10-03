import { sendToInbox } from "@/lib/mail";

export async function POST(req: Request) {
  const form = await req.formData();
  const name = String(form.get("name") ?? "").slice(0, 200);
  const email = String(form.get("email") ?? "").slice(0, 200);
  const message = String(form.get("message") ?? "").slice(0, 5000);
  if (!name || !email || !message) return new Response("Missing fields", { status: 422 });
  await sendToInbox({ name, email, message });
  return Response.redirect(new URL("/contact?sent=1", req.url), 303);
}
