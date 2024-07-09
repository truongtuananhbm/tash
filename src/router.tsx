import { FC } from "react";
import { HashRouter, Route, Routes } from "react-router-dom";
import { IndexPage } from "./pages";
import { ChakraProvider } from "@chakra-ui/react";
import { QueryClient, QueryClientProvider } from "react-query";


const queryClient = new QueryClient();

export const Router: FC = () => {
	return (
		<QueryClientProvider client={queryClient}>
			<ChakraProvider>
				<HashRouter>
					<Routes>
						<Route path="/">
							<Route index element={<IndexPage />} />
						</Route>
					</Routes>
				</HashRouter>
			</ChakraProvider>
		</QueryClientProvider>


	);
};
