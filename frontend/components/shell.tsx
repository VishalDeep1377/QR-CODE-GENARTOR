"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, ArrowUpRight, Command, FolderClock, Gauge, Layers3, Plus, QrCode, ScanLine, Settings2, Sparkles, Upload } from "lucide-react";
const links = [
  { href: "/", label: "Overview", icon: Gauge },
  { href: "/create", label: "Create QR", icon: Plus },
  { href: "/dynamic", label: "Dynamic QR", icon: Activity },
  { href: "/scan", label: "QR Scanner", icon: ScanLine },
  { href: "/bulk", label: "Bulk generator", icon: Upload },
  { href: "/history", label: "My QR codes", icon: FolderClock },
];
export function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  return <div className="app-shell"><aside className="sidebar"><Link href="/" className="brand"><span className="brand-mark"><QrCode size={21}/></span><span>qr<span className="mint">studio</span><small>CREATIVE WORKSPACE</small></span></Link><div className="workspace"><div className="workspace-avatar">V</div><div><b>Personal workspace</b><small>Free plan</small></div><ArrowUpRight size={14} className="muted"/></div><div className="nav-label">WORKSPACE</div><nav>{links.map(({href,label,icon:Icon})=><Link key={href} href={href} className={`nav-link ${path===href?"active":""}`}><Icon size={17}/>{label}{href==="/create"&&<span className="nav-shortcut">⌘ K</span>}</Link>)}</nav><div className="nav-label tools-label">TOOLS</div><Link href="/" className="nav-link"><Layers3 size={17}/>Templates <span className="soon">SOON</span></Link><Link href="/" className="nav-link"><Activity size={17}/>Analytics</Link><Link href="/" className="nav-link"><Settings2 size={17}/>Settings</Link><div className="sidebar-bottom"><div className="upgrade-card"><div className="upgrade-icon"><Sparkles size={17}/></div><b>Make more with QR Studio</b><p>Dynamic links and scan insights are ready to explore.</p><Link href="/create">Explore workspace <ArrowUpRight size={13}/></Link></div><div className="profile"><div className="profile-avatar">VD</div><div><b>Vishal Deep</b><small>Local workspace</small></div><Command size={16} className="muted"/></div></div></aside><main className="main-area"><header className="topbar"><div className="breadcrumb"><span>Workspace</span><span className="slash">/</span><b>{links.find(x=>x.href===path)?.label || "Overview"}</b></div><div className="top-actions"><span className="status-dot"/> <span className="api-status">Local API workspace</span><button className="icon-button" title="Settings"><Settings2 size={17}/></button><div className="top-avatar">VD</div></div></header><div className="page-content">{children}</div></main></div>;
}
