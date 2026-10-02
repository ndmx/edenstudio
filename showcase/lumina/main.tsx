import { Component, useState, type ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import { CodexChamber } from './codex-chamber';
import { principles, type EraKey } from './codex-content';
import './showcase.css';

class SceneBoundary extends Component<{children:ReactNode},{failed:boolean}> {
  state = {failed:false};
  static getDerivedStateFromError() { return {failed:true}; }
  render() { return this.state.failed ? <p role="status">The interactive scene could not load on this device. You can still explore the design system through the package link above.</p> : this.props.children; }
}
function Showcase() {
  const [era,setEra] = useState<EraKey>('atelier');
  const [principle,setPrinciple] = useState('balance');
  const [cycle,setCycle] = useState(0);
  function select(key:string) { setPrinciple(key);setCycle(value=>value+1); }
  return <>
    <div className="showcase-principles" role="group" aria-label="Design principles">
      {principles.map(item=><button key={item.key} aria-pressed={principle===item.key} onClick={()=>select(item.key)}>{item.name}</button>)}
    </div>
    <SceneBoundary><CodexChamber selectedEra={era} onSelectEra={setEra} activePrincipleKey={principle} onSelectPrinciple={select} balanceCycle={cycle} transitionCycle={cycle} sceneMode="preview" sceneCue="Explore color, geometry, and motion." chapterOverlayOpen={false}/></SceneBoundary>
  </>;
}
createRoot(document.getElementById('lumina-showcase')!).render(<Showcase/>);
