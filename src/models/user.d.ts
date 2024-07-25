/*
    用户类型
*/
export type userType = {
    id: number;
    username: string;
    userAccount: string;
    avatarUrl?: string;
    gender: number;
    phone: string;
    email: string;
    userState: number;
    userRole: number;
    planetCode: string;
    tags: string[];
    createTime: string;
    profile?: string;
}