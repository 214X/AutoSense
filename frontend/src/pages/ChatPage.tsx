import React, { useEffect, useState, useRef } from "react";
// Component imports
import AssistantMessageBox from "../components/AssistantMessageBox";
import UserMessageBox from "../components/UserMessageBox";
import ChatInputArea from "../components/ChatInputArea";
import ChatHeader from "../components/ChatHeader";
// Type imports
import type { ChatMessage } from "../types/ChatMessage";

// TODO: Create welcomer message and use it more clear and short code.
// TODO: There is a some mistake in assitant message format. (I think it is about removing newline from the apicall response or markdown)

const ChatPage: React.FC = () => {
    const [inputValue, setInputValue] = useState<string>("");
    const [messages, setMessages] = useState<ChatMessage[]>([
        {
            role: "assistant",
            content: "Hello! I'm Autosense, your personal car asisstant. You can ask me everything about cars.",
            timestamp: new Date().toISOString(),
        }
    ]);
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    // fetching
    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await fetch("/api/chat/fetch-previous-messages");
                const data = await res.json();

                const formatted = data.map((m: any) => ({
                    role: m.role,
                    content: m.content,
                    timestamp: m.timestamp,
                }));

                setMessages(prev => [...prev, ...formatted]);
            } catch (error) {
                console.error("Message fetch error:", error);
            }
        };

        fetchHistory();
    }, []);

    // scroll handling
    useEffect(
        () => {
            messagesEndRef.current?.scrollIntoView();
        }, [messages]
    );

    const handleSend = async () => {
        const trimmed = inputValue.trim();
        if (!trimmed) return;
        setInputValue("");

        const userMessage: ChatMessage = {
            role: "user",
            content: trimmed,
            timestamp: new Date().toISOString()
        };

        const assistantMessage : ChatMessage = {
            role: "assistant",
            content: "",
            timestamp: new Date().toISOString()
        }

        let assistantIndex = -1;

        setMessages(prev => {
            assistantIndex = prev.length + 1;
            return [...prev, userMessage, assistantMessage];
        });

        try {
            const response = await fetch('/api/chat/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: trimmed
                })
            });

            const reader = response.body?.getReader();
            const decoder = new TextDecoder("utf-8");


            let done = false;
            while (!done) {
                const {value, done: resDone} = await reader.read();
                done = resDone;

                if (value) {
                    const chunk = decoder.decode(value, { stream: true });
                    // normalized chunk -> ("data: content\n\n") -> removed "data: " and "\n\n"
                    // I am not sure about is this part should be more complex. I write this for only SSE 
                    let normalizedChunk = chunk.slice("data: ".length, -2);
                    
                    console.log("chunk: ", normalizedChunk);
                    
                    setMessages(prev => {
                        const copy = [...prev];
                        const target = copy[assistantIndex];

                        if (target && target.role === "assistant") {
                            copy[assistantIndex] = {
                                ...target,
                                content: target.content + normalizedChunk,
                            };
                        }

                        return copy;
                    });
                }
            }

            console.log("HTTPS status:", response.status);
        } catch (error) {
            console.error("Stream request error:", error)
        }
    }

    const handleReset = () => {
        try {
            // TODO: check the response (error check)
            const res = fetch("/api/chat/reset", {
                    method: "POST"
            });
            setMessages(([
                {
                    role: "assistant",
                    content: "Hello! I'm Autosense, your personal car asisstant. You can ask me everything about cars.",
                    timestamp: new Date().toISOString(),
                }
            ]));
        } catch (error) {
            console.error(error)
        }
    }

    // PAGE COMPONENT
    return (
        <div className="chat-page">
            {/* Header */}
            <ChatHeader onReset={handleReset} resetDisabled={!(messages.length > 1)}/>

            {/* Messages */}
            <div className="chat-messages">
                <div className="chat-messages">
                    {messages.map((message, index) => (
                        message.role === "assistant" ? (
                            <AssistantMessageBox key={index} content={message.content} />
                        ) : (
                            <UserMessageBox key={index} content={message.content} />
                        )
                    ))}
                    {/* ref for pointing to end of the mssages */}
                    <div ref={messagesEndRef} />
                </div>
            </div>
            {/* UserInputArea */}
            <ChatInputArea 
                value={inputValue} 
                onChange={setInputValue} 
                onSend={handleSend}  />
        </div>
    )
}

export default ChatPage;
