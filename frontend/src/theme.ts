import { extendTheme } from "@chakra-ui/react";

export const theme = extendTheme({
  colors: {
    brand: {
      500: "#ffffff",
      600: "#aaaaaa",
      700: "#5a5a5a",
    },
  },
  styles: {
    global: {
      body: {
        bg: "gray.700",
      },
    },
  },
});
