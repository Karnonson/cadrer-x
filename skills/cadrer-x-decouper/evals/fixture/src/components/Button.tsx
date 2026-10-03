import styles from "./Button.module.css";

type Props = { variant?: "primary" | "ghost" } & React.ButtonHTMLAttributes<HTMLButtonElement>;

export function Button({ variant = "primary", className, ...props }: Props) {
  return <button className={[styles.btn, styles[variant], className].filter(Boolean).join(" ")} {...props} />;
}
