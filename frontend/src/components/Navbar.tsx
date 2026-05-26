import { Box, Button, Flex, Input, Image } from "@chakra-ui/react";
import { login, logout, isAuthenticated, getUsername } from "../utils/auth";

export default function Navbar() {
  const authenticated = isAuthenticated();

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
            maxW="700px"
            mx="auto"
            display="block"
          />
        </Box>

        <Box>
          {authenticated ? (
            <Flex align="center" gap={3}>
              <Box as="span">{getUsername()}</Box>
              <Button colorScheme="red" onClick={logout}>
                Logout
              </Button>
            </Flex>
          ) : (
            <Button colorScheme="teal" onClick={login}>
              Login
            </Button>
          )}
        </Box>
      </Flex>
    </Box>
  );
}
