import { Routes, Route } from "react-router-dom";
import Login from "@/pages/Login";
import Platform from "@/pages/Platform";

// One <Route> per page in src/pages; BrowserRouter already wraps this in main.tsx.
export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Platform />} />
      <Route path="*" element={<Platform />} />
    </Routes>
  );
}
