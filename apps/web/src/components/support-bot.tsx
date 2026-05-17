"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

type Message = { role: "user" | "assistant"; content: string };

export function SupportBot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "I answer questions about this platform using official documentation only. Ask how to monitor agents, adjust budgets, or use control surfaces.",
    },
  ]);
  const [input, setInput] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState({ category: "feature", subject: "", body: "" });

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: userMsg }]);

    const res = await fetch("/api/v1/support/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMsg }),
    });
    const data = await res.json();
    if (data.redirect_to_feedback) {
      setShowFeedback(true);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content:
            "That looks like a strategic request, bug report, or feature ask. Please use the feedback form so we can route it to your tenant in the Master CRM.",
        },
      ]);
      return;
    }
    setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
  };

  const submitFeedback = async () => {
    await fetch("/api/v1/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(feedback),
    });
    setShowFeedback(false);
    setFeedback({ category: "feature", subject: "", body: "" });
    setMessages((m) => [
      ...m,
      { role: "assistant", content: "Feedback logged. An administrator will be notified." },
    ]);
  };

  return (
    <div className="flex h-[480px] flex-col rounded-lg border border-border">
      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
              msg.role === "user" ? "ml-auto bg-primary text-primary-foreground" : "bg-muted"
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>
      {showFeedback ? (
        <div className="space-y-2 border-t border-border p-4">
          <select
            className="w-full rounded border border-border p-2 text-sm"
            value={feedback.category}
            onChange={(e) => setFeedback({ ...feedback, category: e.target.value })}
          >
            <option value="bug">Bug</option>
            <option value="feature">Feature request</option>
            <option value="strategic">Strategic request</option>
          </select>
          <input
            className="w-full rounded border border-border p-2 text-sm"
            placeholder="Subject"
            value={feedback.subject}
            onChange={(e) => setFeedback({ ...feedback, subject: e.target.value })}
          />
          <textarea
            className="w-full rounded border border-border p-2 text-sm"
            placeholder="Details"
            rows={3}
            value={feedback.body}
            onChange={(e) => setFeedback({ ...feedback, body: e.target.value })}
          />
          <Button size="sm" onClick={submitFeedback}>
            Submit to Master CRM
          </Button>
        </div>
      ) : (
        <div className="flex gap-2 border-t border-border p-4">
          <input
            className="flex-1 rounded-md border border-border px-3 py-2 text-sm"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="Ask about the platform..."
          />
          <Button onClick={send}>Send</Button>
        </div>
      )}
    </div>
  );
}
