import styles from "./Alert.module.css";

export function Alert({ tone = "info", children }: { tone?: "info" | "error"; children: React.ReactNode }) {
  return <div className={`${styles.alert} ${styles[tone]}`} role={tone === "error" ? "alert" : undefined}>{children}</div>;
}
