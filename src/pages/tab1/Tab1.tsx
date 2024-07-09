import React, { RefObject, useEffect, useRef, useState } from "react";
import "./tab1.scss";
import P4Q10 from "../../assets/Phuong4Q10.jpeg";

// import { useDownloadExcel } from 'react-export-table-to-excel';
// @ts-ignore
import TableToExcel from "@linways/table-to-excel";


import {
	AbsoluteCenter,
	Divider,
	Box,
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Input,
	Stack,
	FormControl,
	Select,
	Text,
	FormLabel,
	extendTheme,
	ChakraProvider,
	Button,
	useToast,
} from "@chakra-ui/react";

import { myRequest } from "../../utils/axios-utils";
import { cssScrollBar } from "../../utils/my-utils";

interface IMyInutProps {
	label: String,
	element: JSX.Element

}

interface IGroupDT {
	"id": string,
	"name": string,
	"created_at": any
}

interface INeighbour {
	code: string;
	message: string;
	data: INeighbourDT[];
	links: any;
	relationships: any;
	timestamp: string;
}

interface INeighbourDT {
	id: string;
	name: string;
	created_at: string;
}

interface IForces {
	code: string;
	message: string;
	data: IForcesDT[];
	links: any;
	relationships: any;
	timestamp: string;
}

interface IForcesDT {
	id: string;
	name: string;
	unit: string;
	numberBarrel: string;
	typeBarrel_id: string;
	position_id: string;
	worker: string;
	created_at: string;
}

interface IStates {
	code: string;
	message: string;
	data: IStatesDT[];
	links: any;
	relationships: any;
	timestamp: string;
}

interface IStatesDT {
	id: string;
	name: string;
	created_at: string;
}

interface ITableDT {
	id: string;
	name: string;
	address: string;
	garbageMass: string;
	neighbourhood_id: string;
	group_id: string;
	price: string;
	state_id: string;
	force_id: string;
	created_at: string;
}


const activeLabelStyles = {
	transform: "scale(0.85) translateY(-24px)",
};
export const theme = extendTheme({
	components: {
		Form: {
			variants: {
				floating: {
					container: {
						_focusWithin: {
							label: {
								...activeLabelStyles,
							},
						},
						"input:not(:placeholder-shown) + label, .chakra-select__wrapper + label, textarea:not(:placeholder-shown) ~ label": {
							...activeLabelStyles,
						},
						label: {
							top: 0,
							left: 0,
							zIndex: 2,
							position: "absolute",
							backgroundColor: "white",
							pointerEvents: "none",
							mx: 3,
							px: 1,
							my: 2,
							transformOrigin: "left top",
						},
					},
				},
			},
		},
	},
});


export const Tab1: React.FC = () => {
	const [isFetchAll, setIsFetchAll] = useState(false);

	const [groupData, setGroupData] = useState<IGroupDT[]>([]);
	const [neighbourhoodsData, setNeighbourhoodsData] = useState<INeighbourDT[]>([]);
	const [forcesData, setForcesData] = useState<IForcesDT[]>([]);
	const [statesData, setStatesData] = useState<IStatesDT[]>([]);
	const [priceTransport, setPriceTransport] = useState<string>();
	const [garbageMass, setGarbageMass] = useState<string>();

	const refCurID = useRef<string>("");
	const refCurIdx = useRef<number>(99999);
	const refCurObj = useRef<ITableDT>();

	const refPrevTBRow = useRef<string>("");

	const refInputName = useRef<HTMLInputElement>(null);
	const refInputAddr = useRef<HTMLInputElement>(null);
	const refInputNei = useRef<HTMLSelectElement>(null);
	const refInputGroup = useRef<HTMLSelectElement>(null);
	const refInputMass = useRef<HTMLInputElement>(null);
	const refInputPrice = useRef<HTMLInputElement>(null);
	const refInputStates = useRef<HTMLSelectElement>(null);
	const refInputForces = useRef<HTMLSelectElement>(null);

	const refTable = useRef<HTMLTableElement>(null)


	const [isAddBtnLoading, setIsAddBtnLoading] = useState(false);
	const [isDelBtnLoading, setIsDelBtnLoading] = useState(false);
	const [isSearchBtnLoading, setIsSearchBtnLoading] = useState(false);
	const [isUpdateBtnLoading, setIsUpdateBtnLoading] = useState(false);
	const [isExportBtnLoading, setIsExportBtnLoading] = useState(false);

	const toast = useToast();

	const [tableDT, setTableDT] = useState<ITableDT[]>([]);

	// const

	const MyTable: React.FC = () => {
		return (
			<TableContainer style={{ height: "calc(100vh - 260px)", overflow: "auto" }}
							className="border-[2px] rounded-[5px]" css={cssScrollBar} ref={refTable}>
				<Table variant="simple" >
					<Thead className="bg-gray-200" position="sticky" top={0} zIndex="docked">
						<Tr>
							<Th></Th>
							<Th>Tên</Th>
							<Th>Địa chỉ</Th>
							<Th>Khu phố</Th>
							<Th>Nhóm</Th>
							<Th>Giá trị chuyển rác</Th>
							<Th>Giá vận chuyển rác</Th>
							<Th>Tình trạng đóng tiền</Th>
							<Th>Lực lượng đang thu gom rác</Th>
						</Tr>
					</Thead>
					<Tbody display="contents">
						{tableDT.map((i, ii) => {
							return (
								<Tr id={i.id} className="tb-row cursor-pointer hover:bg-gray-100" onClick={(e) => {
									onClickR(ii, i);
									const prevR = document.getElementById(refPrevTBRow.current)!;
									if (prevR) prevR.style.background = "";

									const curR = document.getElementById(i.id)!;

									curR.style.background = "rgb(243 244 246)";
									refPrevTBRow.current = i.id;

								}} key={i.id}>
									<Td>{ii + 1}</Td>
									<Td>{i.name}</Td>
									<Td>{i.address}</Td>
									<Td>{neighbourhoodsData.find((x) => x.id === i.neighbourhood_id)?.name}</Td>
									<Td>{groupData.find((x) => x.id === i.group_id)?.name}</Td>
									<Td>{i.garbageMass}</Td>
									<Td>{formatCurrency(i.price)}đ</Td>
									<Td>{statesData.find((x) => x.id === i.state_id)?.name}</Td>
									<Td>{forcesData.find((x) => x.id === i.force_id)?.name}</Td>
								</Tr>
							);
						})}

					</Tbody>
				</Table>
			</TableContainer>
		);
	};
	const fetchGroups = async () => {
		const req = await myRequest({ url: "/Tash-Manager/groups", method: "patch" });
		if (req.status != 200)
			setGroupData([{
				"id": "string",
				"name": "_",
				"created_at": "None"
			}]);
		setGroupData([{
			"id": "string",
			"name": "_",
			"created_at": "None"
		},...req.data.data]);

	};

	const fetchNeighbourhoods = async () => {
		const req = await myRequest({ url: "/Tash-Manager/neighbourhoods", method: "patch" });
		if (req.status != 200)
			setNeighbourhoodsData([{
				"id": "string",
				"name": "_",
				"created_at": "None"
			}]);
		setNeighbourhoodsData([{
			"id": "string",
			"name": "_",
			"created_at": "None"
		},...req.data.data]);
	};

	const fetchGetForces = async () => {
		const req = await myRequest({ url: "/Tash-Manager/forces", method: "patch" });
		if (req.status != 200)
			setForcesData([{
				id: "string",
				name: "_",
				unit: "string",
				numberBarrel: "string",
				typeBarrel_id: "string",
				position_id: "string",
				worker: "string",
				created_at: "string"
			}]);
		setForcesData([{
			id: "string",
			name: "_",
			unit: "string",
			numberBarrel: "string",
			typeBarrel_id: "string",
			position_id: "string",
			worker: "string",
			created_at: "string"
		},...req.data.data]);
	};

	const fetchGetStates = async () => {
		const req = await myRequest({ url: "/Tash-Manager/states", method: "patch" });
		if (req.status != 200)
			setStatesData([]);
		setStatesData([{
			"id": "string",
			"name": "_",
			"created_at": "None"
		},...req.data.data]);
	};

	const fetchTableDT = async () => {
		const req = await myRequest({ url: "Tash-Manager/owners", method: "patch" });
		if (req.status != 200)
			setTableDT([]);
		const _tb = req.data.data;
		for (const _i of _tb) _i.price = String(Number(_i.price));

		setTableDT(_tb || []);
	};


	const fetchAll = () => {
		setIsFetchAll(true);
		setIsAddBtnLoading(false)
		setIsDelBtnLoading(false)
		setIsExportBtnLoading(false)
		setIsSearchBtnLoading(false)
		setIsUpdateBtnLoading(false)
		setAllDefault()
		Promise.all([fetchGroups(), fetchNeighbourhoods(), fetchGetForces(), fetchGetStates(), fetchTableDT()]).then(_ => {
				setIsFetchAll(false);
			},
		);
	};

	useEffect(() => {
		fetchAll();

	}, []);

	const myToast = (tit: string, des: string, type: any) => {
		toast({
			title: tit,
			description: des,
			status: type,
			duration: 5000,
			isClosable: true,
		});
	};

	const objName: {
		[key: string]: string
	} = {
		name: "Tên",
		address: "Địa chỉ",
		neighbourhood_id: "Khu phố",
		group_id: "Nhóm",
		garbageMass: "Giá trị chuyển rác",
		price: "Giá vận chuyển",
		state_id: "Tình trạng đóng tiền",
		force_id: "Lực lượng thu gom rác",
	};

	const defaultObj: { [key: string]: any } = {
		"name": "string",
		"address": "string",
		"garbageMass": 0,
		"price": 0,
		"neighbourhood_id": "string",
		"group_id": "string",
		"state_id": "string",
		"force_id": "string",
	};


	const getAllInput = (): { [key: string]: any } => {
		return {
			name: refInputName.current?.value,
			address: refInputAddr.current?.value,
			neighbourhood_id: refInputNei.current?.value,
			group_id: refInputGroup.current?.value,
			garbageMass: refInputMass.current?.value,
			price: refInputPrice.current?.value,
			state_id: refInputStates.current?.value,
			force_id: refInputForces.current?.value,
		};
	};

	const setDefault = (obj: { [key: string]: any }) => {
		for (const [key, value] of Object.entries(obj)) {
			if (!value?.trim().length) {
				obj[key] = defaultObj[key];
			}
		}
		return obj;

	};



	const setAllDefault = () => {

		setRefValue(refInputName, "");
		setRefValue(refInputAddr, "");
		setRefValue(refInputNei, "string");
		setRefValue(refInputGroup,"string");
		setRefValue(refInputMass, "");
		setRefValue(refInputPrice, "");
		setRefValue(refInputStates, "string");
		setRefValue(refInputForces, "string");

	};

	const setRefValue = (ref: RefObject<HTMLInputElement | HTMLSelectElement>, value: any) => {
		if (ref.current) {
			ref.current.value = value;
		}
	};
	const onClickR = (idx: number, obj: ITableDT) => {
		refCurID.current = obj.id;
		refCurIdx.current = idx;
		refCurObj.current = obj;
		setRefValue(refInputName, obj.name);
		setRefValue(refInputAddr, obj.address);
		setRefValue(refInputNei, obj.neighbourhood_id);
		setRefValue(refInputGroup, obj.group_id);
		setRefValue(refInputMass, obj.garbageMass);
		setRefValue(refInputPrice, formatCurrency(obj.price));
		setRefValue(refInputStates, obj.state_id);
		setRefValue(refInputForces, obj.force_id);

	};

	const selectKey: { [key: string]: any } = {
		"neighbourhood_id": "string",
		"group_id": "string",
		"state_id": "string",
		"force_id": "string",
	};


	const insertOrUpdate = (type: string) => {

		const obj = getAllInput();
		for (const [key, value] of Object.entries(obj)) {
			if ((!value?.trim().length) || (value?.trim() === "string" && selectKey[key] )){
				myToast(`${objName[key]} không được trống !`, "", "error");
				return;
			}
		}
		obj["price"] = Number(obj["price"]?.replaceAll(",", ""));
		obj["garbageMass"] = Number(obj["garbageMass"]);


		if (type === "insert") {
			setIsAddBtnLoading(true);
			myRequest({
				url: "/Tash-Manager/owners", method: "post", data: JSON.stringify(obj), headers: {
					"accept": "application/json",
					"Content-Type": "application/json",
				},
			})
				.then(() => {
					fetchTableDT();

					myToast(`Thêm thành công`, "", "success");
					setIsAddBtnLoading(false);

				})
				.catch(() => {
					myToast(`Thêm thất bại`, "", "error");
					setIsAddBtnLoading(false);
				});
		} else if (type === "update") {
			setIsUpdateBtnLoading(true);


			myRequest({
				url: `/Tash-Manager/owners/${refCurID.current}`, method: "put", data: JSON.stringify(obj), headers: {
					"accept": "application/json",
					"Content-Type": "application/json",
				},
			})
				.then(() => {
					fetchTableDT();
					setAllDefault();

					myToast(`Sửa thành công`, "", "success");
					setIsUpdateBtnLoading(false);

				})
				.catch(() => {
					myToast(`Sửa thất bại`, "", "error");
					setIsUpdateBtnLoading(false);
				});
		}
	};
	const formatCurrency = (val: string) => {
		let value = val.replace(/\D/g, "");
		if (value.length)
			value = Number(value.replace(/,/g, "")).toLocaleString();
		return value;
	};
	const searchOwner = () => {
		setIsSearchBtnLoading(true);

		const obj = setDefault(getAllInput())

		// const obj = {
		// 	...getAllInput(),
		// 	name: refInputName.current?.value.trim().length ? refInputName.current?.value.trim()  : "string",
		// 	address: refInputAddr.current?.value.trim().length ? refInputAddr.current?.value.trim() : "string",
		// 	garbageMass: refInputMass.current?.value.length ? refInputMass.current?.value : 0,
		// 	price: refInputPrice.current?.value.length ?  refInputPrice.current?.value : 0,
		// };




		obj["price"] = Number(String(obj["price"])?.replaceAll(",", ""));
		obj["garbageMass"] = Number(obj["garbageMass"]);

		setTableDT([]);

		myRequest({
			url: "/Tash-Manager/owner", method: "patch", data: JSON.stringify(obj), headers: {
				"accept": "application/json",
				"Content-Type": "application/json",
			},
		})
			.then((response: { data: { data: any; }; }) => {
				const _tb = response.data.data;
				for (const _i of _tb) _i.price = String(Number(_i.price));
				setTableDT(_tb || []);

				setIsSearchBtnLoading(false);

			})
			.catch(() => {
				setIsSearchBtnLoading(false);
			});
	};

	const onDelete = () => {
		if (refCurID.current) {
			setIsDelBtnLoading(true);
			myRequest({
				url: `/Tash-Manager/owners/${refCurID.current}`, method: "DELETE", headers: {
					"accept": "application/json",

				},
			})
				.then(() => {
					const dt = tableDT.filter((_, ii) => ii != refCurIdx.current);
					setTableDT(dt);
					setAllDefault();

					myToast(`Xóa thành công`, "", "success");

					setIsDelBtnLoading(false);

				})
				.catch(() => {
					myToast(`Xóa thất bại`, "", "error");

					setIsDelBtnLoading(false);
				});
		}
	};

	// const { onDownload } = useDownloadExcel({
	// 	currentTableRef: refTable.current,
	// 	filename: 'Users table',
	// 	sheet: 'Users'
	// })

	const exportXL = () => {
		TableToExcel.convert(refTable.current, {
			name: `Table_${new Date().toLocaleString()}`,
			sheet: {
				name: "Sheet 1"
			}
		});
		// const obj = refCurObj.current
		// if (obj) {
		// 	setIsExportBtnLoading(true);
		//
		// 	myRequest({
		// 		url: `/Tash-Manager/download/owners`,
		// 		method: "PATCH",
		// 		data: JSON.stringify(refCurObj.current),
		// 		responseType: "blob",
		// 		headers: {
		// 			"accept": "application/json",
		// 			"Content-Type": "application/json",
		// 		},
		// 	})
		// 		.then((response) => {
		//
		// 			var blob = new Blob([response.data], {
		// 				type: response.headers["content-type"],
		// 			});
		// 			const link = document.createElement("a");
		// 			link.href = window.URL.createObjectURL(blob);
		//
		// 			link.download = `report_${obj.name}.xlsx`;
		// 			link.click();
		//
		// 			myToast(`Xuất excel thành công`, "", "success");
		//
		// 			setIsExportBtnLoading(false);
		//
		// 		})
		// 		.catch((_) => {
		// 			myToast(`Xuất excel thất bại`, "", "error");
		//
		// 			setIsExportBtnLoading(false);
		// 		});
		//
		// }
		//
	};


	return (
		<div className="tab1">

			<div className="header flex flex-row items-center gap-5 justify-center">
				<img
					id="icon"
					src={P4Q10}
					height={30}
					width={200}
					alt="amethyst"
				/>
				<p className="text-2xl font-black text-gray-900 dark:text-white " style={{ color: "black" }}>
					Quản Lý Chủ Nguồn Thải
				</p>

			</div>

			<div className="content flex justify-between">
				<div className="con-left w-[68%]">
					<Box position="relative" padding="10">
						<Divider />
						<AbsoluteCenter bg="white" px="4">

							<p className="text-lg font-semibold text-gray-900 dark:text-white">Kết quả</p>
						</AbsoluteCenter>
					</Box>

					<MyTable />

				</div>

				<div className="con-center w-[2px] h-auto bg-gray-300 mt-[25px]" />
				{/* divider */}

				<div className="con-right w-[29%]">
					<Box position="relative" padding="10">
						<Divider />
						<AbsoluteCenter bg="white" px="4">
							<p className="text-lg font-semibold text-gray-900 dark:text-white"> Chủ nguồn thải</p>

						</AbsoluteCenter>
					</Box>

					<ChakraProvider theme={theme}>
						<Stack spacing={5}>
							<FormControl variant="floating" id="name" isRequired={true}>
								<Input placeholder=" " required={true} ref={refInputName} />
								<FormLabel className={"form-label"}>Tên</FormLabel>
							</FormControl>
							<FormControl variant="floating" id="name" isRequired={true}>
								<Input placeholder=" " ref={refInputAddr} />
								<FormLabel className={"form-label"}>Địa chỉ</FormLabel>
							</FormControl>
							<div className="flex flex-col">
								<Text className="ml-3">Khu phố</Text>
								<Select size="md" isRequired={true} ref={refInputNei}>
									{neighbourhoodsData.map((i: INeighbourDT) => <option key={i.id}
																						 value={i.id}>{i.name}</option>)}
								</Select>
							</div>

							<div className="">
								<Text className="ml-3">Nhóm</Text>
								<Select size="md" isRequired={true} ref={refInputGroup}>
									{groupData.map((i: IGroupDT) => <option key={i.id} value={i.id}>{i.name}</option>)}
								</Select>
							</div>

							<FormControl variant="floating" id="" isRequired={true}>
								<Input placeholder={" "} ref={refInputMass} onChange={(e) => {
									// refInputMass.current.value =
									setRefValue(refInputMass, e.target.value.replace(/\D/g, ""));
									// setGarbageMass(e.target.value.replace(/\D/g, ""));

								}} />

								<FormLabel className={"form-label"}>Giá trị chuyển rác</FormLabel>
							</FormControl>

							<FormControl variant="floating" id="" isRequired={true}>
								<Input placeholder={" "} ref={refInputPrice} onChange={(e) => {
									// setPriceTransport(formatCurrency(e.target.value));
									setRefValue(refInputPrice, formatCurrency(e.target.value));

								}} />

								<FormLabel className={"form-label"}>Giá vận chuyển rác</FormLabel>
							</FormControl>


							<div className="">
								<Text className="ml-3">Tình trạng đóng tiền</Text>
								<Select size="md" ref={refInputStates}>
									{statesData.map((i: IStatesDT) => <option key={i.id}
																			  value={i.id}>{i.name}</option>)}
								</Select>
							</div>

							<div className="">
								<Text className="ml-3">Lực lượng đang thu gom rác</Text>
								<Select size="md" ref={refInputForces}>
									{forcesData.map((i: IForcesDT) => <option key={i.id}
																			  value={i.id}>{i.name}</option>)}
								</Select>
							</div>

							<div className="flex gap-2">
								<Button colorScheme="teal" variant="outline" isLoading={isAddBtnLoading}
										onClick={() => insertOrUpdate("insert")}>
									Thêm
								</Button>
								<Button colorScheme="teal" isLoading={isDelBtnLoading} variant="outline"
										onClick={() => onDelete()}>
									Xóa
								</Button>
								<Button colorScheme="teal" isLoading={isSearchBtnLoading} variant="outline"
										onClick={() => searchOwner()}>
									Tìm
								</Button>
								<Button colorScheme="teal" isLoading={isUpdateBtnLoading} variant="outline"
										onClick={() => insertOrUpdate("update")}>
									Sửa
								</Button>
								<Button colorScheme="teal" isLoading={isExportBtnLoading} variant="outline"
										onClick={() => exportXL()}>
									Xuất
								</Button>
							</div>

						</Stack>

						{/*reload*/}
						<div className="flex justify-end w-full">
							<Button isLoading={isFetchAll} onClick={fetchAll} className="mt-10"
									colorScheme="gray">{isFetchAll ? "Loading..." : "↻"}</Button>

						</div>
					</ChakraProvider>

				</div>
			</div>

		</div>


	);

};