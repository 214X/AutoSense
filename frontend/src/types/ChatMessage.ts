export type Role = "user" | "assistant";

export type ChatMessage = {
    role: Role;
    message: string;
    timestamp: string;
}