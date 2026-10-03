import nodemailer from "nodemailer";

const transport = nodemailer.createTransport({
  host: "smtp-relay.brevo.com",
  port: 587,
  auth: { user: process.env.BREVO_SMTP_USER, pass: process.env.BREVO_SMTP_PASS },
});

export async function sendToInbox(m: { name: string; email: string; message: string }) {
  await transport.sendMail({
    from: "site@ateliernord.fr",
    to: process.env.STUDIO_INBOX,
    replyTo: m.email,
    subject: `New project request from ${m.name}`,
    text: m.message,
  });
}
