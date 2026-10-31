"use client";

import React, {
  Children,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { motion, useInView } from "framer-motion";
import { cn } from "@/lib/utils";
import "./terminal.css";

const SequenceContext = createContext(null);
const useSequence = () => useContext(SequenceContext);

const ItemIndexContext = createContext(null);
const useItemIndex = () => useContext(ItemIndexContext);

export const Terminal = ({
  children,
  className,
  title = "bash",
  sequence = true,
  startOnView = true,
}) => {
  const containerRef = useRef(null);
  const isInView = useInView(containerRef, {
    amount: 0.2,
    once: true,
  });

  const [activeIndex, setActiveIndex] = useState(0);
  const sequenceHasStarted = sequence ? !startOnView || isInView : false;

  const childArray = useMemo(() => Children.toArray(children), [children]);

  const completeItem = (index) => {
    if (index === activeIndex) {
      setActiveIndex((prev) => prev + 1);
    }
  };

  const contextValue = useMemo(() => {
    if (!sequence) return null;
    return {
      completeItem,
      activeIndex,
      sequenceStarted: sequenceHasStarted,
    };
  }, [sequence, activeIndex, sequenceHasStarted]);

  return (
    <div
      ref={containerRef}
      className={cn("magicui-terminal", className)}
    >
      <div className="magicui-terminal-inner">
        <div className="magicui-terminal-header">
          <div className="magicui-terminal-dots">
            <span className="magicui-terminal-dot magicui-terminal-dot--red" />
            <span className="magicui-terminal-dot magicui-terminal-dot--yellow" />
            <span className="magicui-terminal-dot magicui-terminal-dot--green" />
          </div>
          {title && <span className="magicui-terminal-title">{title}</span>}
        </div>
        <SequenceContext.Provider value={contextValue}>
          <div className="magicui-terminal-body">
            {childArray.map((child, index) => (
              <ItemIndexContext.Provider key={index} value={index}>
                {child}
              </ItemIndexContext.Provider>
            ))}
          </div>
        </SequenceContext.Provider>
      </div>
    </div>
  );
};

export const AnimatedSpan = ({
  children,
  delay = 0,
  className,
  startOnView = false,
  ...props
}) => {
  const elementRef = useRef(null);
  const isInView = useInView(elementRef, {
    amount: 0.2,
    once: true,
  });
  const sequence = useSequence();
  const itemIndex = useItemIndex();
  const [hasStarted, setHasStarted] = useState(false);

  useEffect(() => {
    if (!sequence || itemIndex === null) return;
    if (!sequence.sequenceStarted) return;
    if (hasStarted) return;

    if (sequence.activeIndex === itemIndex) {
      if (delay > 0) {
        const timer = setTimeout(() => setHasStarted(true), delay);
        return () => clearTimeout(timer);
      }
      setHasStarted(true);
    }
  }, [sequence, hasStarted, itemIndex, delay]);

  const shouldAnimate = sequence ? hasStarted : startOnView ? isInView : true;

  return (
    <motion.div
      ref={elementRef}
      initial={{ opacity: 0, y: -4 }}
      animate={shouldAnimate ? { opacity: 1, y: 0 } : { opacity: 0, y: -4 }}
      transition={{
        duration: 0.25,
        delay: sequence ? 0 : delay / 1000,
        ease: "easeOut",
      }}
      className={cn("magicui-terminal-span", className)}
      onAnimationComplete={() => {
        if (!sequence || itemIndex === null) return;
        sequence.completeItem(itemIndex);
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export const TypingAnimation = ({
  children,
  className,
  duration = 45,
  delay = 0,
  as: Component = "span",
  startOnView = true,
  ...props
}) => {
  const textContent = typeof children === "string" ? children : String(children ?? "");
  const [displayedText, setDisplayedText] = useState("");
  const [started, setStarted] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const elementRef = useRef(null);

  const sequence = useSequence();
  const itemIndex = useItemIndex();

  const isInView = useInView(elementRef, {
    amount: 0.2,
    once: true,
  });

  useEffect(() => {
    if (sequence && itemIndex !== null) {
      if (sequence.sequenceStarted && sequence.activeIndex === itemIndex) {
        const timer = setTimeout(() => {
          setStarted(true);
        }, delay);
        return () => clearTimeout(timer);
      }
      return;
    }

    if (!startOnView || isInView) {
      const timer = setTimeout(() => {
        setStarted(true);
      }, delay);
      return () => clearTimeout(timer);
    }
  }, [sequence, itemIndex, startOnView, isInView, delay]);

  useEffect(() => {
    if (!started) return;

    let i = 0;
    const typingEffect = setInterval(() => {
      if (i < textContent.length) {
        setDisplayedText(textContent.substring(0, i + 1));
        i++;
      } else {
        clearInterval(typingEffect);
        setIsFinished(true);
        if (sequence && itemIndex !== null) {
          sequence.completeItem(itemIndex);
        }
      }
    }, duration);

    return () => clearInterval(typingEffect);
  }, [textContent, duration, started, sequence, itemIndex]);

  return (
    <Component
      ref={elementRef}
      className={cn(
        "magicui-terminal-typing",
        isFinished && "typing-complete",
        className
      )}
      {...props}
    >
      {displayedText}
    </Component>
  );
};

export default Terminal;

