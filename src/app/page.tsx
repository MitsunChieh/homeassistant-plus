import { Dashboard } from "@/components/Dashboard";

export default function Home() {
  return (
    <main className="max-w-4xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-100 mb-6">Home</h1>
      <Dashboard />
    </main>
  );
}
