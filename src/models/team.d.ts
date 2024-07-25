/*
    队伍类型
*/
export type teamType = {
    id: number;
    name: string;
    description: string;
    maxNum: number;
    expireTime?: string;
    userId: number;
    status: number;
    password?: string; 
    createTime: Date;
    updateTime: Date;
    createUser?: userType;
    hasJoin: boolean;
    userInfo: List;
}