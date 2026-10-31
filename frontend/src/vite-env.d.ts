/// <reference types="vite/client" />

declare module "next/image" {
  import { FC, CSSProperties } from "react";

  export interface ImageProps {
    src: string;
    alt?: string;
    width?: number | string;
    height?: number | string;
    className?: string;
    style?: CSSProperties;
    priority?: boolean;
    fill?: boolean;
    [key: string]: any;
  }

  const Image: FC<ImageProps>;
  export default Image;
}

