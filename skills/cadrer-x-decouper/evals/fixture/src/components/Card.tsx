import Link from "next/link";
import styles from "./Card.module.css";

type Props = { title: string; meta?: string; href?: string; children?: React.ReactNode };

export function Card({ title, meta, href, children }: Props) {
  const body = (
    <>
      <p className={styles.title}>{title}</p>
      {children}
      {meta && <p className={styles.meta}>{meta}</p>}
    </>
  );
  return href ? <Link className={styles.card} href={href}>{body}</Link> : <div className={styles.card}>{body}</div>;
}
