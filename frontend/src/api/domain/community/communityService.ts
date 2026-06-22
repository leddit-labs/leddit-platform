import client from "../../client";
import { endpoints } from "../../endpoints";
import type { Community } from "./community";

export const communityService = {
	async getById(id: string): Promise<Community> {
		const response = await client.get<Community>(
			endpoints.communities.byId(id)
		);

		return response.data;
	},
};