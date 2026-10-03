export default function Contact() {
  return (
    <form method="post" action="/api/contact">
      <input name="name" required />
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  );
}
