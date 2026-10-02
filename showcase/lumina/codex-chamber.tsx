"use client";

import { startTransition, useEffect, useMemo, useState } from "react";
import type { CSSProperties, PointerEvent } from "react";
import { eras, principles, type EraKey } from "./codex-content";
import { CodexScene } from "./codex-scene";

type ChamberStyle = CSSProperties;
type SceneMode = "preview" | "theater";

type CodexChamberProps = {
  selectedEra: EraKey;
  onSelectEra: (era: EraKey) => void;
  activePrincipleKey: string;
  onSelectPrinciple: (principleKey: string) => void;
  balanceCycle: number;
  transitionCycle: number;
  sceneMode: SceneMode;
  sceneCue: string;
  chapterOverlayOpen: boolean;
};

const eraClassMap: Record<EraKey, string> = {
  atelier: "lumina-chamber--atelier",
  memphis: "lumina-chamber--memphis",
  brutalist: "lumina-chamber--brutalist",
};

const interactionNotes: Record<string, string> = {
  balance: "Balance distributes visual weight around a stable center.",
  contrast: "Contrast brings the selected element forward through light and hierarchy.",
  rhythm: "Rhythm uses repetition and orbital motion to establish a cadence.",
  unity: "Unity draws the moving parts into one coherent composition.",
};


export function CodexChamber({
  selectedEra,
  onSelectEra,
  activePrincipleKey,
  onSelectPrinciple,
  balanceCycle,
  transitionCycle,
  sceneMode,
  sceneCue,
  chapterOverlayOpen,
}: CodexChamberProps) {
  const [pointer, setPointer] = useState({ x: 0.5, y: 0.32 });
  const [liteMode, setLiteMode] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const activePrinciple =
    principles.find((principle) => principle.key === activePrincipleKey) ?? principles[0];
  const activeEra = eras.find((era) => era.key === selectedEra) ?? eras[0];
  const scrollPercent = Math.round(scrollProgress * 100);

  const chamberStyle = useMemo(
    () =>
      ({
        ["--pointer-x" as string]: String(pointer.x),
        ["--pointer-y" as string]: String(pointer.y),
        ["--accent-color" as string]: activePrinciple.accent,
      }) as ChamberStyle,
    [activePrinciple.accent, pointer.x, pointer.y],
  );

  const liveAnnouncement = useMemo(
    () =>
      `${activePrinciple.name} active in ${activeEra.name}. ${sceneMode === "theater" ? "Theater mode active." : "Preview mode active."} ${chapterOverlayOpen ? "Full chapter open." : "Chapter shell closed."} ${isTransitioning ? "Transition live." : "Transition settled."} ${interactionNotes[activePrincipleKey]} ${
        reducedMotion ? "Reduced motion scene active." : liteMode ? "Lite scene active." : "Full scene active."
      } Narrative depth ${scrollPercent} percent.`,
    [
      activeEra.name,
      activePrinciple.name,
      activePrincipleKey,
      chapterOverlayOpen,
      isTransitioning,
      liteMode,
      reducedMotion,
      sceneMode,
      scrollPercent,
    ],
  );

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");

    function updateViewportState() {
      const nextLiteMode = media.matches || window.innerWidth < 900;
      const maxScroll = Math.max(window.innerHeight * 1.2, 1);
      const nextProgress = Math.min(window.scrollY / maxScroll, 1);

      startTransition(() => {
        setLiteMode(nextLiteMode);
        setReducedMotion(media.matches);
        setScrollProgress(nextProgress);
      });
    }

    updateViewportState();
    media.addEventListener("change", updateViewportState);
    window.addEventListener("resize", updateViewportState);
    window.addEventListener("scroll", updateViewportState, { passive: true });

    return () => {
      media.removeEventListener("change", updateViewportState);
      window.removeEventListener("resize", updateViewportState);
      window.removeEventListener("scroll", updateViewportState);
    };
  }, []);

  useEffect(() => {
    if (transitionCycle === 0) {
      return;
    }

    const frame = window.requestAnimationFrame(() => {
      setIsTransitioning(true);
    });
    const timeout = window.setTimeout(() => setIsTransitioning(false), 1150);

    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(timeout);
    };
  }, [transitionCycle]);

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    if (reducedMotion) {
      return;
    }

    const rect = event.currentTarget.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width;
    const y = (event.clientY - rect.top) / rect.height;
    setPointer({ x, y });
  }

  return (
    <section
      className={[
        "lumina-chamber",
        eraClassMap[selectedEra],
        isTransitioning ? "is-transitioning" : "",
      ].join(" ")}
      style={chamberStyle}
      onPointerMove={handlePointerMove}
      onPointerLeave={() => setPointer({ x: 0.5, y: 0.32 })}
      aria-labelledby="codex-heading"
      data-scene-mode={sceneMode}
      data-transitioning={isTransitioning ? "true" : "false"}
    >
      <p className="lumina-sr-only" aria-live="polite">
        {liveAnnouncement}
      </p>

      <div className="lumina-chamber__glow" />
      <div className="lumina-chamber__mist" />
      <div className="lumina-chamber__grid" />

      <div className="lumina-chamber__panel">
        <div className="lumina-chamber__controls">
          <div>
            <p className="lumina-kicker">Visual style</p>
            <h2 id="codex-heading" className="lumina-panel-title">
              Lumina Chamber
            </h2>
          </div>

          <div className="lumina-toggle-group" role="group" aria-label="Select an era for the chamber">
            {eras.map((era) => (
              <button
                key={era.key}
                type="button"
                
                aria-pressed={selectedEra === era.key}
                className={selectedEra === era.key ? "is-active" : undefined}
                onClick={() => onSelectEra(era.key)}
              >
                {era.name}
              </button>
            ))}
          </div>
        </div>

        <div className="lumina-chamber__viewport">
          <div className="lumina-chamber__hud" aria-hidden="true">
            <span>{sceneMode === "theater" ? "Theater mode" : "Preview mode"}</span>
            <span>{isTransitioning ? "Transition live" : `Depth ${scrollPercent}%`}</span>
            <span>{chapterOverlayOpen ? "Chapter live" : liteMode ? "Lite scene" : "Full scene"}</span>
          </div>

          <CodexScene
            era={selectedEra}
            activePrincipleKey={activePrincipleKey}
            balanceCycle={balanceCycle}
            transitionCycle={transitionCycle}
            liteMode={liteMode}
            reducedMotion={reducedMotion}
            pointer={pointer}
            scrollProgress={scrollProgress}
            sceneMode={sceneMode}
            chapterOverlayOpen={chapterOverlayOpen}
            onSelectPrinciple={onSelectPrinciple}
          />
        </div>

        <div className="lumina-chamber__footer">
          <div className="lumina-status">
            <p className="lumina-kicker">Current principle</p>
            <h3>{activePrinciple.name}</h3>
            <p>{interactionNotes[activePrincipleKey]}</p>
          </div>

          <div className="lumina-era-note">
            <p className="lumina-kicker">Scene cue</p>
            <h3>{sceneMode === "theater" ? "Exhibit mode engaged" : activeEra.mood}</h3>
            <p>{sceneMode === "theater" ? sceneCue : activeEra.descriptor}</p>
            <p className="lumina-render-note">
              {reducedMotion ? "Reduced motion scene active" : isTransitioning ? "Transition live" : liteMode ? "Lite scene active" : "Full scene active"} • narrative depth {scrollPercent}%.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
