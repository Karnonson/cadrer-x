import styles from "./Field.module.css";

type Props = { label: string; hint?: string; error?: string } & React.InputHTMLAttributes<HTMLInputElement>;

export function Field({ label, hint, error, id, ...input }: Props) {
  const inputId = id ?? input.name;
  return (
    <div className={styles.field}>
      <label className={styles.label} htmlFor={inputId}>{label}</label>
      <input className={styles.input} id={inputId} aria-invalid={error ? true : undefined} {...input} />
      {hint && !error && <span className={styles.hint}>{hint}</span>}
      {error && <span className={styles.error}>{error}</span>}
    </div>
  );
}
