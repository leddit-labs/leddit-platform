import { extendTheme } from "@chakra-ui/react"

export const theme = extendTheme({
	colors: {
		brand: {
			500: "#ffffff",
			600: "#aaaaaa",
			700: "#5a5a5a",
		},
	},
})
console.log("THEME LOADED:", theme)
console.log("THEME LOADED:", JSON.stringify(theme, null, 2))