import { SimplifiedSession } from "@/interfaces/history";

export const HistoryList = () => {
  // TODO: fetch sessions from backend
  const SESSIONS: SimplifiedSession[] = [
    {
      id: "1",
      lastActive: "2024-01-01",
    },
    {
      id: "2",
      lastActive: "2024-01-02",
    },
    {
      id: "3",
      lastActive: "2024-01-03",
    },
    {
      id: "4",
      lastActive: "2024-01-04",
    },
    {
      id: "5",
      lastActive: "2024-01-05",
    },
    {
      id: "6",
      lastActive: "2024-01-06",
    },
    {
      id: "7",
      lastActive: "2024-01-07",
    },
    {
      id: "8",
      lastActive: "2024-01-08",
    },
    {
      id: "9",
      lastActive: "2024-01-09",
    },
    {
      id: "10",
      lastActive: "2024-01-10",
    },
    {
      id: "11",
      lastActive: "2024-01-11",
    },
    {
      id: "12",
      lastActive: "2024-01-12",
    },
  ];

  return (
    <div className="flex flex-col gap-2 h-full">
      <h1 className="font-bold text-xl mb-4">History</h1>
      <div className="flex flex-col gap-2 overflow-y-auto">
        {/* On click, close history and load history onto chat with date on top or something that indicates it's history, block send? or load id? */}
        {SESSIONS.map((session) => (
          <button
            key={session.id}
            className="flex flex-row justify-between bg-gray-100 hover:bg-gray-200 p-2 rounded-md"
          >
            <div>{session.lastActive}</div>
          </button>
        ))}
      </div>
    </div>
  );
};
