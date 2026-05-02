import { Box, Button, Flex, Input, Image } from "@chakra-ui/react";

export default function Navbar() {
  return (
    <Box bg="gray.800" color="white" px={4} py={3}>
      <Flex align="center" justify="space-between">
        <Box>
          <Image src="/logo.svg" maxH="60px" maxW="100%" objectFit="contain" />
        </Box>

        <Box flex="1" mx={6}>
          <Input
            placeholder="Search..."
            bg="whiteAlpha.200"
            color="white"
            maxW="600px"
            mx="auto"
            display="block"
          />
        </Box>

        <Box>
          <Button colorScheme="teal">Login</Button>
        </Box>
      </Flex>
    </Box>
  );
}
