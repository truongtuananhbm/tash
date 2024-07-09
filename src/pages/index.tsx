import { FC } from "react";
import { Layout } from "../components/Layout";

import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'
import { Tab1 } from "./tab1/Tab1";
import { Tab2 } from "./tab2/Tab2";

export const IndexPage: FC = () => {
	return (
		<Layout>
			{/*<div>Hello main (new update!)</div>*/}
			<Tabs>
				<TabList>
					<Tab>Chủ Nguồn Thải</Tab>
					<Tab>Lực Lượng Thu Gom</Tab>
				</TabList>

				<TabPanels>
					<TabPanel>
						<Tab1/>
					</TabPanel>
					<TabPanel>
						<Tab2/>
					</TabPanel>

				</TabPanels>
			</Tabs>
		</Layout>


	);
};
