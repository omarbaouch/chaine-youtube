import React from 'react';
import {AbsoluteFill, interpolate, staticFile, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import type {EpisodeProps, Scene} from './types';
import {ScenePlan} from './ScenePlan';
import {Grain} from './effets/Grain';

const presentation = (t: Scene['transition']) => {
  if (t === 'glissement') return slide({direction: 'from-right'});
  if (t === 'balayage') return wipe({direction: 'from-left'});
  return fade();
};

const Musique: React.FC<{src: string; volume: number}> = ({src, volume}) => {
  const {durationInFrames, fps} = useVideoConfig();
  return (
    <Audio
      name="Musique"
      src={staticFile(src)}
      loop
      volume={(f) =>
        interpolate(f, [0, fps * 1.5, durationInFrames - fps * 2, durationInFrames], [0, volume, volume, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      }
    />
  );
};

export const Episode: React.FC<EpisodeProps> = (props) => {
  const {scenes, dureeTransition, musique, grain} = props;
  const items: React.ReactNode[] = [];
  scenes.forEach((s, i) => {
    if (i > 0 && s.transition !== 'coupe') {
      items.push(
        <TransitionSeries.Transition
          key={`t-${s.id}`}
          presentation={presentation(s.transition)}
          timing={linearTiming({durationInFrames: dureeTransition})}
        />,
      );
    }
    items.push(
      <TransitionSeries.Sequence key={s.id} name={`${s.id} · ${s.type}`} durationInFrames={s.duree}>
        <ScenePlan scene={s} etalonnage={props.etalonnage} />
      </TransitionSeries.Sequence>,
    );
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <TransitionSeries>{items}</TransitionSeries>
      {musique ? <Musique src={musique.src} volume={musique.volume} /> : null}
      {grain ? <Grain /> : null}
    </AbsoluteFill>
  );
};

export const dureeTotale = (p: EpisodeProps) => {
  const transitions = p.scenes.filter((s, i) => i > 0 && s.transition !== 'coupe').length;
  return Math.max(1, p.scenes.reduce((a, s) => a + s.duree, 0) - transitions * p.dureeTransition);
};
