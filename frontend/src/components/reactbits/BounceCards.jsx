'use client';

import { useEffect, useRef } from 'react';

import './BounceCards.css';

const PATTERN = [1, 0.5, -0.3, -1, 0.2, 0.75, -0.6, 0.35, -0.85, 0.1];

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

const parseTransform = value => {
  if (typeof value !== 'string') return null;
  const rotate = value.match(/rotate\(\s*(-?[\d.]+)deg\s*\)/);
  const translate = value.match(/translate\(\s*(-?[\d.]+)px(?:\s*,\s*(-?[\d.]+)px)?\s*\)/);
  return {
    x: translate ? Number(translate[1]) : 0,
    y: translate && translate[2] ? Number(translate[2]) : 0,
    rotate: rotate ? Number(rotate[1]) : 0
  };
};

const toCard = item => (typeof item === 'string' ? { src: item, alt: '' } : { src: item?.src, alt: item?.alt ?? '' });

export default function BounceCards({
  images = [],
  className = '',
  style,
  containerWidth = 400,
  containerHeight = 400,
  cardSize = 200,
  spread = 85,
  rotation = 10,
  arc = 0,
  animationDelay = 0.5,
  animationStagger = 0.06,
  bounciness = 0.6,
  enableHover = true,
  pushDistance = 160,
  hoverScale = 1.06,
  borderWidth = 5,
  borderColor = '#ffffff',
  radius = 25,
  shadow = true,
  transformStyles,
  onCardClick
}) {
  const rootRef = useRef(null);
  const cardRefs = useRef([]);
  const wakeRef = useRef(null);
  const cards = images.map(toCard);
  const count = cards.length;
  const middle = (count - 1) / 2;
  const reach = Math.max(1, middle);
  const slots = cards.map((_, i) => {
    const custom = transformStyles ? parseTransform(transformStyles[i]) : null;
    if (custom) return custom;
    const offset = i - middle;
    return {
      x: offset * spread,
      y: arc * (offset / reach) ** 2,
      rotate: rotation * PATTERN[i % PATTERN.length]
    };
  });
  const settings = {
    slots,
    cardSize: Math.max(10, cardSize),
    delay: Math.max(0, animationDelay),
    stagger: Math.max(0, animationStagger),
    bounciness: clamp(bounciness, 0, 1),
    enableHover,
    pushDistance,
    hoverScale: clamp(hoverScale, 0.5, 2),
    clickable: typeof onCardClick === 'function'
  };
  const settingsRef = useRef(settings);
  settingsRef.current = settings;
  const clickRef = useRef(onCardClick);
  clickRef.current = onCardClick;

