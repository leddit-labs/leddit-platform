import { useQuery } from "@tanstack/react-query";
import { communityService } from "./communityService";

export function useCommunity(communityId: string) {
	return useQuery({
		queryKey: ["community", communityId],
		queryFn: () => communityService.getById(communityId),
	});
}