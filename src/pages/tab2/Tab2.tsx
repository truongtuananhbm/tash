import React, { RefObject, useEffect, useRef, useState } from "react";
import "./tab2.scss";
import P4Q10 from "../../assets/Phuong4Q10.jpeg";

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


interface ITypeBarrel {
	id: string;
	name: string;
	created_at: string;
}

interface IPosition {
	id: string;
	name: string;
	created_at: string;
}

interface ITableDT {
	id: string;
	name: string;
	unit: string;
	numberBarrel: string;
	typeBarrel_id: string;
	position_id: string;
	worker: string;
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


export const Tab2: React.FC = () => {
	const [isFetchAll, setIsFetchAll] = useState(false);

	const [typeBarrel, setTypeBarrel] = useState<ITypeBarrel[]>([]);
	const [position, setPosition] = useState<IPosition[]>([]);

	const refInputName = useRef<HTMLInputElement>(null);
	const refInputUnit = useRef<HTMLInputElement>(null);
	const refInputNumBarrel = useRef<HTMLInputElement>(null);
	const refInputTypeBarrel = useRef<HTMLSelectElement>(null);
	const refInputPosition = useRef<HTMLSelectElement>(null);
	const refInputWorker = useRef<HTMLInputElement>(null);

	const [isAddBtnLoading, setIsAddBtnLoading] = useState(false);
	const [isDelBtnLoading, setIsDelBtnLoading] = useState(false);
	const [isSearchBtnLoading, setIsSearchBtnLoading] = useState(false);
	const [isUpdateBtnLoading, setIsUpdateBtnLoading] = useState(false);

	const [tableDT, setTableDT] = useState<ITableDT[]>([]);

	const refCurID = useRef<string>("");
	const refCurIdx = useRef<number>(99999);
	const refCurObj = useRef<ITableDT>();
	const refPrevTBRow = useRef<string>("");

	const toast = useToast();


	const MyTable: React.FC = () => {
		return (
			<TableContainer style={{ height: "calc(100vh - 260px)", overflow: "auto" }}
							className="border-[2px] rounded-[5px]" css={cssScrollBar}>
				<Table variant="simple">
					<Thead className="bg-gray-200" position="sticky" top={0} zIndex="docked">
						<Tr>
							<Th></Th>
							<Th>Tên</Th>
							<Th>Đơn vị tư cách pháp nhân</Th>
							<Th>Số lượng thùng</Th>
							<Th>Loại thùng</Th>
							<Th>Vị trí tập kết rác</Th>
							<Th>Số lượng nhân viên</Th>
						</Tr>
					</Thead>
					<Tbody>
						{tableDT.map((i, ii) => {
							return (
								<Tr id={i.id} className="tb-row cursor-pointer hover:bg-gray-100" onClick={(_) => {
									onClickR(ii, i);
									const prevR = document.getElementById(refPrevTBRow.current)!;
									if (prevR) prevR.style.background = "";

									const curR = document.getElementById(i.id)!;

									curR.style.background = "rgb(243 244 246)";
									refPrevTBRow.current = i.id;

								}} key={i.id}>
									<Td>{ii + 1}</Td>
									<Td>{i.name}</Td>
									<Td>{i.unit}</Td>
									<Td>{i.numberBarrel}</Td>
									<Td>{typeBarrel.find((x) => x.id == i.typeBarrel_id)?.name}</Td>
									<Td>{position.find((x) => x.id == i.position_id)?.name}</Td>
									<Td>{i.worker}</Td>
								</Tr>
							);
						})}


					</Tbody>

				</Table>
			</TableContainer>
		);
	};

	const myToast = (tit: string, des: string, type: any) => {
		toast({
			title: tit,
			description: des,
			status: type,
			duration: 5000,
			isClosable: true,
		});
	};

	const setAllDefault = () => {
		setRefValue(refInputName, "");
		setRefValue(refInputUnit, "");
		setRefValue(refInputNumBarrel, "");
		setRefValue(refInputTypeBarrel,"string");
		setRefValue(refInputPosition, "string");
		setRefValue(refInputWorker, "");
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
		setRefValue(refInputUnit, obj.unit);
		setRefValue(refInputNumBarrel, obj.numberBarrel);
		setRefValue(refInputTypeBarrel, obj.typeBarrel_id);
		setRefValue(refInputPosition, obj.position_id);
		setRefValue(refInputWorker, obj.worker);

	};

	const objName: {
		[key: string]: string
	} = {
		name: "Tên",
		unit: "Đơn vị",
		numberBarrel: "Số lượng thùng",
		typeBarrel_id: "Loại thùng",
		position_id: "Vị trí",
		worker: "Số lượng nhân viên",
	};

	const defaultObj: { [key: string]: any } = {
		name: "string",
		unit: "string",
		numberBarrel: 0,
		typeBarrel_id: "string",
		position_id: "string",
		worker: 0,
	};

	const setDefault = (obj: { [key: string]: any }) => {
		for (const [key, value] of Object.entries(obj)) {
			if (!value?.trim().length) {
				obj[key] = defaultObj[key];
			}
		}
		return obj;

	};
	const getAllInput = (): { [key: string]: any } => {
		return {
			name: refInputName.current?.value,
			unit: refInputUnit.current?.value,
			numberBarrel: refInputNumBarrel.current?.value,
			typeBarrel_id: refInputTypeBarrel.current?.value,
			position_id: refInputPosition.current?.value,
			worker: refInputWorker.current?.value,

		};
	};
	const selectKey: { [key: string]: any } = {
		typeBarrel_id: "string",
		position_id: "string",
	};


	const insertOrUpdate = (type: string) => {

		const obj = getAllInput();

		for (const [key, value] of Object.entries(obj)) {
			if ((!value?.trim().length) || (value?.trim() == "string" && selectKey[key] )) {
				myToast(`${objName[key]} không được trống !`, "", "error");
				return;
			}
		}

		if (type == "insert") {
			setIsAddBtnLoading(true);
			myRequest({
				url: "/Tash-Manager/forces", method: "post", data: JSON.stringify(obj), headers: {
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
		} else if (type == "update") {
			setIsUpdateBtnLoading(true);


			myRequest({
				url: `/Tash-Manager/forces/${refCurID.current}`, method: "put", data: JSON.stringify(obj), headers: {
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

	const searchForces = () => {
		setIsSearchBtnLoading(true);

		const obj = setDefault(getAllInput())

		// {
		// 	"name": "string",
		// 	"unit": "string",
		// 	"numberBarrel": 0,
		// 	"typeBarrel_id": "string",
		// 	"position_id": "string",
		// 	"worker": 0
		// }

		//			name: refInputName.current?.value,
		// 			unit: refInputUnit.current?.value,
		// 			numberBarrel: refInputNumBarrel.current?.value,
		// 			typeBarrel_id: refInputTypeBarrel.current?.value,
		// 			position_id: refInputPosition.current?.value,
		// 			worker: refInputWorker.current?.value,

		setTableDT([]);

		myRequest({
			url: "/Tash-Manager/force", method: "patch", data: JSON.stringify(obj), headers: {
				"accept": "application/json",
				"Content-Type": "application/json",
			},
		})
			.then((response: { data: { data: any; }; }) => {

				setTableDT(response.data.data || []);
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
				url: `/Tash-Manager/forces/${refCurID.current}`, method: "DELETE", headers: {
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

	const fetchTypeBarrel = async () => {
		const req = await myRequest({ url: "/Tash-Manager/type_barrels", method: "patch" });
		if (req.status != 200)
			setTypeBarrel([{
				"id": "string",
				"name": "_",
				"created_at": "None"
			}]);
		setTypeBarrel([{
			"id": "string",
			"name": "_",
			"created_at": "None"
		},...req.data.data]);
	};

	const fetchPositions = async () => {

		const req = await myRequest({ url: "/Tash-Manager/positions", method: "patch" });
		if (req.status != 200)
			setPosition([{
				"id": "string",
				"name": "_",
				"created_at": "None"
			}]);
		setPosition([{
			"id": "string",
			"name": "_",
			"created_at": "None"
		},...req.data.data]);
	};
	const fetchTableDT = async () => {
		const req = await myRequest({ url: "Tash-Manager/forces", method: "patch" });
		if (req.status != 200)
			setTableDT([]);

		setTableDT(req.data.data || []);
	};

	const fetchAll = () => {
		setIsFetchAll(true);
		setIsAddBtnLoading(false)
		setIsDelBtnLoading(false)
		setIsSearchBtnLoading(false)
		setIsUpdateBtnLoading(false)
		setAllDefault()
		Promise.all([fetchTypeBarrel(), fetchPositions(), fetchTableDT()]).then(_ => {
				setIsFetchAll(false);
			},
		);
	};

	useEffect(() => {
		fetchAll();

	}, []);

	return (
		<div className="tab2">
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
				<div className="con-left w-[68%] ">
					<Box position="relative" padding="10">
						<Divider />
						<AbsoluteCenter bg="white" px="4">
							<div className="text-lg font-semibold text-gray-900 dark:text-white">Kết quả</div>
						</AbsoluteCenter>
					</Box>

					<MyTable />


				</div>

				<div className="con-center w-[2px] h-auto bg-gray-300 mt-[25px]" />
				{/* divider */}

				<div className="con-right w-[29%]">
					<Box position="relative" paddingY={10} paddingX={2}>
						<Divider />
						<AbsoluteCenter bg="white" px={0}>
							<div className="text-lg text-center font-semibold text-gray-900 dark:text-white">Lực lượng
								thu gom rác
							</div>

						</AbsoluteCenter>
					</Box>

					<ChakraProvider theme={theme}>
						<Stack spacing={5}>
							<FormControl variant="floating" isRequired={true}>
								<Input placeholder=" " ref={refInputName} />
								<FormLabel className={"form-label"}>Tên</FormLabel>
							</FormControl>

							<FormControl variant="floating" isRequired={true}>
								<Input placeholder=" " ref={refInputUnit} />
								<FormLabel className={"form-label"}>Đơn vị</FormLabel>
							</FormControl>

							<FormControl variant="floating" isRequired={true}>
								<Input placeholder=" " ref={refInputNumBarrel} onChange={(e) => {
									setRefValue(refInputNumBarrel, e.target.value.replace(/\D/g, ""));

								}} />
								<FormLabel className={"form-label"}>Số lượng thùng</FormLabel>
							</FormControl>

							<div className="flex flex-col">
								<Text className="ml-3">Loại thùng</Text>
								<Select size="md" ref={refInputTypeBarrel}>
									{typeBarrel.map((i: ITypeBarrel) => <option key={i.id}
																				value={i.id}>{i.name}</option>)}
								</Select>
							</div>

							<div className="flex flex-col">
								<Text className="ml-3">Vị trí</Text>

								<Select size="md" ref={refInputPosition}>
									{position.map((i: IPosition) => <option key={i.id}
																			value={i.id}>{i.name}</option>)}
								</Select>
							</div>


							<FormControl variant="floating" id="" isRequired={true}>
								<Input ref={refInputWorker} placeholder={" "} onChange={(e) => {
									setRefValue(refInputWorker, e.target.value.replace(/\D/g, ""));

								}} />

								<FormLabel className={"form-label"}>Số lượng nhân viên</FormLabel>
							</FormControl>


							<div className="flex gap-2 justify-end">
								<Button colorScheme="teal" variant="outline" isLoading={isAddBtnLoading}
										onClick={() => insertOrUpdate("insert")}>
									Thêm
								</Button>
								<Button colorScheme="teal" variant="outline" isLoading={isDelBtnLoading}
										onClick={onDelete}>
									Xóa
								</Button>
								<Button colorScheme="teal" variant="outline" isLoading={isSearchBtnLoading}
										onClick={searchForces}>
									Tìm
								</Button>
								<Button colorScheme="teal" variant="outline" isLoading={isUpdateBtnLoading}
										onClick={() => insertOrUpdate("update")}>
									Sửa
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