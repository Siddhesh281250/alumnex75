import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { ArrowRight, CheckCircle2, CloudSun, LockKeyhole, ShieldCheck, Sparkles } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiPost } from "@/lib/api";
import type { User } from "@/lib/types";

const demoAccounts = [
  { role: "Trainee", email: "trainee@capacityconnect.gov.in", name: "Dr. Ananya Sharma", color: "bg-cyan-500" },
  { role: "Trainer", email: "trainer@capacityconnect.gov.in", name: "Dr. Rajesh Kumar", color: "bg-indigo-500" },
  { role: "Admin", email: "admin@capacityconnect.gov.in", name: "Shri Vikramaditya", color: "bg-amber-500" },
];

function errorMessage(error: unknown) {
  const body = (error as { body?: { detail?: unknown } })?.body;
  const detail = body?.detail;
  return typeof detail === "string" ? detail : "We could not start the demo session.";
}

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState(demoAccounts[0].email);
  const [password, setPassword] = useState("Demo@123");
  const loginMutation = useMutation({
    mutationFn: () => apiPost<User>("/auth/login", { email, password }),
    onSuccess: () => {
      toast.success("Secure demo session started", { description: "Welcome to Capacity Connect." });
      navigate("/", { replace: true });
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  const chooseAccount = (account: (typeof demoAccounts)[number]) => {
    setEmail(account.email);
    setPassword("Demo@123");
    toast.info(`${account.role} demo selected`, { description: account.name });
  };

  return (
    <main className="min-h-svh overflow-hidden bg-[#f6f8fb] text-[#0b192c]" data-testid="login-page">
      <div className="grid min-h-svh lg:grid-cols-[1.05fr_.95fr]">
        <section className="relative hidden overflow-hidden bg-[#0b192c] px-10 py-10 text-white lg:flex lg:flex-col lg:justify-between xl:px-16">
          <div className="absolute -right-36 top-10 h-96 w-96 rounded-full border border-cyan-300/20 bg-cyan-400/10 blur-3xl" />
          <div className="absolute -bottom-32 left-1/4 h-80 w-80 rounded-full border border-indigo-300/20 bg-indigo-500/15 blur-3xl" />
          <div className="relative z-10 flex items-center gap-3" data-testid="login-brand-lockup">
            <span className="grid size-11 place-items-center rounded-2xl bg-cyan-400 text-[#0b192c] shadow-lg shadow-cyan-400/20"><CloudSun className="size-6" /></span>
            <div><p className="text-sm font-semibold tracking-[.2em] text-cyan-200">IMD • MoES</p><p className="font-heading text-lg font-bold">CAPACITY CONNECT</p></div>
          </div>
          <div className="relative z-10 max-w-xl pb-12">
            <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-white/5 px-3 py-1.5 text-xs font-semibold uppercase tracking-[.18em] text-cyan-200"><Sparkles className="size-3.5" /> Capacity intelligence platform</p>
            <h1 className="font-heading text-5xl font-extrabold leading-[1.02] tracking-tight xl:text-7xl" data-testid="login-hero-title">Build the capability behind every forecast.</h1>
            <p className="mt-6 max-w-lg text-lg leading-8 text-slate-300" data-testid="login-hero-description">Personalize learning, connect expertise and translate training signals into stronger organizational capacity.</p>
            <div className="mt-9 grid grid-cols-3 gap-3" data-testid="login-impact-stats">
              {[['2,500+', 'learners'], ['120+', 'trainers'], ['15k', 'resources']].map(([value, label]) => <div key={label} className="rounded-2xl border border-white/10 bg-white/5 p-4"><p className="font-heading text-2xl font-bold text-white">{value}</p><p className="mt-1 text-xs uppercase tracking-wider text-slate-400">{label}</p></div>)}
            </div>
          </div>
          <p className="relative z-10 text-xs text-slate-500" data-testid="login-demo-note">Prototype environment • All learning data shown is demo/sample data</p>
        </section>

        <section className="flex items-center justify-center px-5 py-8 sm:px-10">
          <div className="w-full max-w-lg">
            <div className="mb-8 flex items-center gap-3 lg:hidden" data-testid="mobile-login-brand"><span className="grid size-10 place-items-center rounded-xl bg-[#0b192c] text-cyan-300"><CloudSun className="size-5" /></span><div><p className="text-xs font-bold tracking-[.2em] text-[#005c97]">IMD • MoES</p><p className="font-heading font-bold">CAPACITY CONNECT</p></div></div>
            <div className="mb-8"><p className="mb-3 text-xs font-bold uppercase tracking-[.2em] text-[#005c97]">Secure demo access</p><h2 className="font-heading text-4xl font-extrabold tracking-tight text-[#0b192c]" data-testid="login-form-title">Enter the command centre.</h2><p className="mt-3 leading-7 text-slate-500" data-testid="login-form-description">Use a prefilled role to explore how learning signals become actionable capacity intelligence.</p></div>

            <div className="mb-6 grid gap-3" data-testid="demo-account-list">
              {demoAccounts.map((account) => <button key={account.role} type="button" onClick={() => chooseAccount(account)} data-testid={`demo-account-${account.role.toLowerCase()}-button`} className={`group flex items-center justify-between rounded-2xl border p-4 text-left transition-colors duration-200 ${email === account.email ? "border-[#005c97] bg-white shadow-md shadow-slate-200" : "border-slate-200 bg-white/70 hover:border-slate-300"}`}><span className="flex items-center gap-3"><span className={`grid size-10 place-items-center rounded-xl text-sm font-bold text-white ${account.color}`}>{account.name.split(" ").map((part) => part[0]).join("").slice(0, 2)}</span><span><span className="block text-sm font-semibold text-[#0b192c]">{account.name}</span><span className="mt-0.5 block text-xs text-slate-500">{account.role} workspace</span></span></span>{email === account.email ? <CheckCircle2 className="size-5 text-[#00a896]" /> : <ArrowRight className="size-4 text-slate-300 transition-transform duration-200 group-hover:translate-x-1" />}</button>)}
            </div>

            <form onSubmit={(event) => { event.preventDefault(); loginMutation.mutate(); }} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/60 sm:p-8" data-testid="login-form">
              <label className="mb-2 block text-sm font-semibold text-slate-700" htmlFor="email">Work email</label>
              <Input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="h-12 rounded-xl" data-testid="login-email-input" />
              <label className="mb-2 mt-5 block text-sm font-semibold text-slate-700" htmlFor="password">Password</label>
              <Input id="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="h-12 rounded-xl" data-testid="login-password-input" />
              <Button type="submit" disabled={loginMutation.isPending} className="mt-6 h-12 w-full rounded-xl bg-[#005c97] text-white hover:bg-[#004b7c]" data-testid="login-submit-button"><LockKeyhole className="size-4" />{loginMutation.isPending ? "Starting secure session…" : "Open demo workspace"}<ArrowRight className="ml-auto size-4" /></Button>
              <div className="mt-5 flex items-start gap-2 rounded-xl bg-slate-50 p-3 text-xs leading-5 text-slate-500" data-testid="login-security-note"><ShieldCheck className="mt-0.5 size-4 shrink-0 text-[#00a896]" />Sessions use secure httpOnly cookies in this prototype. Never use demo credentials for production systems.</div>
            </form>
            <p className="mt-6 text-center text-xs text-slate-400" data-testid="login-footer">Learn. Build Skills. Connect Expertise. Measure Impact.</p>
          </div>
        </section>
      </div>
    </main>
  );
}